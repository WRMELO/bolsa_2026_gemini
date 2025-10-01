"""
Update pipeline: raw (01_bruto) -> adequado (02_adequado) -> SSOT (02_curado)

- Incremental ingestion up to the most recent date available (Investing/yfinance)
- Standardize into 02_adequado (schema, TZ, dedupe)
- Build SSOT Parquets: panel_close.parquet and panel_volume.parquet in 02_curado

Notes:
- Designed to run daily. Safe on re-runs (idempotent by (ticker,date)).
- If stage CSVs exist in 00_data/minio_panels_stage (panel_close_Y*.csv / panel_volume_Y*.csv),
  SSOT prefers concatenating them. Otherwise, it pivots from 02_adequado.
"""

from __future__ import annotations

import argparse
import sys
import os
from pathlib import Path
from datetime import datetime, timedelta, date
from typing import Iterable, Tuple, Optional

import pandas as pd

# Optional deps: investpy, yfinance
try:
    import investpy  # type: ignore
except Exception:  # pragma: no cover
    investpy = None
try:
    import yfinance as yf  # type: ignore
except Exception:  # pragma: no cover
    yf = None

try:
    from zoneinfo import ZoneInfo
except Exception:  # Python<3.9 fallback
    from backports.zoneinfo import ZoneInfo  # type: ignore


TZ_SP = ZoneInfo("America/Sao_Paulo")


# ---------------------- TICKERS & INDICATORS ----------------------
TICKERS_B3 = [
    "ABEV3.SA", "B3SA3.SA", "BBAS3.SA", "CSNA3.SA", "CPLE6.SA", "ELET3.SA", "GGBR4.SA",
    "HAPV3.SA", "ITUB4.SA", "LREN3.SA", "PETR4.SA", "PRIO3.SA", "PSSA3.SA", "RAIL3.SA",
    "RDOR3.SA", "SBSP3.SA", "SUZB3.SA", "TAEE11.SA", "TIMS3.SA", "UGPA3.SA", "VALE3.SA",
    "VIVT3.SA", "WEGE3.SA", "TOTS3.SA",
]

INDICATORS = {
    "^BVSP": "_bvsp",
    "EWZ": "ewz",
    "^GSPC": "_gspc",
    "^VIX": "_vix",
    "DX-Y.NYB": "dx-y.nyb",
    "^TNX": "_tnx",
    "BZ=F": "bz=f",
}


# ---------------------- HELPERS ----------------------
def project_root() -> Path:
    # 02_src/ -> project root
    return Path(__file__).resolve().parent.parent


def pick_dir(*candidates: Path) -> Path:
    """Return first existing dir among candidates; if none exist, create the first one."""
    for c in candidates:
        if c.exists():
            return c
    # fallback: create first
    first = candidates[0]
    first.mkdir(parents=True, exist_ok=True)
    return first


def safe_to_datetime_sp(values) -> pd.DatetimeIndex:
    idx = pd.DatetimeIndex(pd.to_datetime(values, errors="coerce"))
    if idx.tz is None:
        idx = idx.tz_localize(TZ_SP)
    else:
        idx = idx.tz_convert(TZ_SP)
    return idx


def normalize_df(df: pd.DataFrame, ticker_label: str, cut_min: date | None, cut_max: date | None) -> pd.DataFrame:
    rename = {
        "Date": "date",
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Adj Close": "adj_close",
        "Volume": "volume",
    }
    df = df.rename(columns=rename)
    # datetime_sp (TZ_SP)
    if "date" in df.columns:
        dt_idx = safe_to_datetime_sp(df["date"])  # type: ignore
    elif "Date" in df.columns:
        dt_idx = safe_to_datetime_sp(df["Date"])  # type: ignore
    else:
        dt_idx = safe_to_datetime_sp(df.index)

    out = df.reset_index(drop=True).copy()
    ts = pd.Series(dt_idx)
    out["datetime_sp"] = ts.values
    out["date"] = pd.to_datetime(ts).dt.date.astype(str)
    out["ticker"] = ticker_label

    if cut_min is not None:
        out = out[out["date"] >= cut_min.strftime("%Y-%m-%d")]
    if cut_max is not None:
        out = out[out["date"] <= cut_max.strftime("%Y-%m-%d")]

    for c in ["open", "high", "low", "close", "volume"]:
        if c not in out.columns:
            out[c] = pd.NA

    out = out[["ticker", "date", "open", "high", "low", "close", "volume", "datetime_sp"]]
    out.drop_duplicates(subset=["ticker", "date"], inplace=True)
    return out


def to_investing_symbol(b3_symbol: str) -> str:
    return b3_symbol.upper().replace(".SA", "")


def fetch_b3(b3_symbol: str, start: date, end: date) -> pd.DataFrame:
    if investpy is None and yf is None:
        raise RuntimeError("Neither investpy nor yfinance is available.")
    sym = to_investing_symbol(b3_symbol)
    f_str = start.strftime('%d/%m/%Y'); t_str = end.strftime('%d/%m/%Y')
    # Try investpy first
    if investpy is not None:
        try:
            res = investpy.search_quotes(text=sym, products=['stocks'], countries=['brazil'])
            qlist = res if isinstance(res, list) else ([res] if res else [])
            if qlist:
                pick = next((q for q in qlist if getattr(q, 'symbol', '').upper() == sym.upper()), qlist[0])
                df = pick.retrieve_historical_data(from_date=f_str, to_date=t_str, as_json=False, order='descending')
                if df is not None and not df.empty:
                    return normalize_df(df, b3_symbol.upper(), start, end)
            df2 = investpy.get_stock_historical_data(stock=sym, country='brazil', from_date=f_str, to_date=t_str, as_json=False, order='descending')
            if df2 is not None and not df2.empty:
                return normalize_df(df2, b3_symbol.upper(), start, end)
        except Exception:
            pass
    # Fallback yfinance
    if yf is None:
        raise RuntimeError("yfinance not available for fallback")
    tkr = yf.Ticker(b3_symbol)
    dfy = tkr.history(start=start.strftime('%Y-%m-%d'), end=(end + timedelta(days=1)).strftime('%Y-%m-%d'), interval='1d', auto_adjust=False)
    if dfy is None or dfy.empty:
        raise RuntimeError(f"Sem dados para {b3_symbol}")
    return normalize_df(dfy, b3_symbol.upper(), start, end)


def fetch_indicator(yf_symbol: str, db_symbol: str, start: date, end: date) -> pd.DataFrame:
    if yf is None:
        raise RuntimeError("yfinance is required for indicators")
    tkr = yf.Ticker(yf_symbol)
    df = tkr.history(start=start.strftime('%Y-%m-%d'), end=(end + timedelta(days=1)).strftime('%Y-%m-%d'), interval='1d', auto_adjust=False)
    if df is None or df.empty:
        raise RuntimeError(f"Sem dados para {yf_symbol}")
    return normalize_df(df, db_symbol, start, end)


def parquet_name_for_stock(sym: str) -> str:
    return f"{sym.lower().replace('.', '_')}_1d.parquet"


def parquet_name_for_indicator(db_label: str) -> str:
    return f"{db_label.replace('.', '_').lower()}_1d.parquet"


def detect_dirs(root: Path) -> Tuple[Path, Path, Path, Path]:
    # Try both naming conventions used in the project
    raw_dir = pick_dir(root / "00_data" / "01_bruto", root / "00_data" / "01_raw")
    adequado_dir = pick_dir(root / "00_data" / "02_adequado", root / "00_data" / "02_processed")
    curado_dir = pick_dir(root / "00_data" / "02_curado")
    stage_dir = pick_dir(root / "00_data" / "minio_panels_stage")
    return raw_dir, adequado_dir, curado_dir, stage_dir


def last_available_date(pq_path: Path) -> Optional[date]:
    if not pq_path.exists():
        return None
    try:
        df = pd.read_parquet(pq_path, columns=["date"])  # only date
        if df.empty:
            return None
        dmax = pd.to_datetime(df["date"], errors="coerce").max()
        if pd.isna(dmax):
            return None
        return dmax.date()
    except Exception:
        return None


def daterange_incremental(last_date: Optional[date], end_date: date, floor_start: date) -> Tuple[date, date]:
    if last_date is None:
        return floor_start, end_date
    start = last_date + timedelta(days=1)
    if start > end_date:
        start = end_date
    return start, end_date


def step_ingest_raw(raw_dir: Path, start_floor: date, end_date: date) -> None:
    print("== Etapa 1: Ingestão RAW (01_bruto)")
    raw_dir.mkdir(parents=True, exist_ok=True)

    # Stocks (B3)
    for sym in TICKERS_B3:
        out_pq = raw_dir / parquet_name_for_stock(sym)
        last_dt = last_available_date(out_pq)
        start_dt, end_dt = daterange_incremental(last_dt, end_date, start_floor)
        print(f"  [B3] {sym} -> {start_dt}..{end_dt}")
        if last_dt is not None and start_dt >= end_dt:
            print("   - já atualizado (sem novas datas)")
            continue
        try:
            df_inc = fetch_b3(sym, start_dt, end_dt)
            if out_pq.exists():
                base = pd.read_parquet(out_pq)
                merged = pd.concat([base, df_inc], ignore_index=True)
                merged.drop_duplicates(subset=["ticker", "date"], inplace=True)
                merged.to_parquet(out_pq, index=False)
            else:
                df_inc.to_parquet(out_pq, index=False)
            print(f"   - gravado: {out_pq}")
        except Exception as e:
            print(f"   ! erro {sym}: {e}")

    # Indicators (yfinance)
    for yf_sym, db_sym in INDICATORS.items():
        out_pq = raw_dir / parquet_name_for_indicator(db_sym)
        last_dt = last_available_date(out_pq)
        start_dt, end_dt = daterange_incremental(last_dt, end_date, start_floor)
        print(f"  [IND] {yf_sym} ({db_sym}) -> {start_dt}..{end_dt}")
        if last_dt is not None and start_dt >= end_dt:
            print("   - já atualizado (sem novas datas)")
            continue
        try:
            df_inc = fetch_indicator(yf_sym, db_sym, start_dt, end_dt)
            if out_pq.exists():
                base = pd.read_parquet(out_pq)
                merged = pd.concat([base, df_inc], ignore_index=True)
                merged.drop_duplicates(subset=["ticker", "date"], inplace=True)
                merged.to_parquet(out_pq, index=False)
            else:
                df_inc.to_parquet(out_pq, index=False)
            print(f"   - gravado: {out_pq}")
        except Exception as e:
            print(f"   ! erro {yf_sym}: {e}")


def step_build_adequado(raw_dir: Path, adequado_dir: Path) -> None:
    print("== Etapa 2: Padronização 02_adequado")
    adequado_dir.mkdir(parents=True, exist_ok=True)
    files = sorted(raw_dir.glob("*.parquet"))
    for p in files:
        try:
            df = pd.read_parquet(p)
            ren = {"Date":"date","Open":"open","High":"high","Low":"low","Close":"close","Adj Close":"adj_close","Volume":"volume"}
            df = df.rename(columns=ren)
            # ticker
            if "ticker" not in df.columns or df["ticker"].isna().any():
                name = p.name
                if name.endswith("_1d.parquet"):
                    tk = name[:-len("_1d.parquet")].replace("_sa"," ").replace("_"," ").strip().replace(" ", "").upper()
                else:
                    tk = name.upper()
                df["ticker"] = tk
            # date normalization (datetime_sp preferred)
            if "datetime_sp" in df.columns:
                s = pd.to_datetime(df["datetime_sp"], errors="coerce")
                df["date"] = pd.to_datetime(df.get("date", s), errors="coerce").dt.date.astype(str)
            else:
                df["date"] = pd.to_datetime(df.get("date"), errors="coerce").dt.date.astype(str)
            for c in ["open","high","low","close","volume"]:
                if c not in df.columns:
                    df[c] = pd.NA
            df = df[["ticker","date","open","high","low","close","volume","datetime_sp"]]
            df.drop_duplicates(subset=["ticker","date"], inplace=True)
            out = adequado_dir / p.name
            df.to_parquet(out, index=False)
            print("  - adequado:", out)
        except Exception as e:
            print("  ! erro em", p.name, e)


def build_ssot_from_adequado(metric: str, adequado_dir: Path, curado_dir: Path) -> Path:
    """Always build SSOT directly from 02_adequado (ignores stage CSVs)."""
    assert metric in ("close", "volume")
    curado_dir.mkdir(parents=True, exist_ok=True)
    out_parquet = curado_dir / f"panel_{metric}.parquet"
    out_manifest = curado_dir / f"panel_{metric}_manifest.json"

    files = sorted(adequado_dir.glob("*.parquet"))
    if not files:
        raise FileNotFoundError("Nenhum arquivo em 02_adequado para construir SSOT.")
    all_rows = []
    for p in files:
        df = pd.read_parquet(p)
        ren = {"Date":"date","Open":"open","High":"high","Low":"low","Close":"close","Adj Close":"adj_close","Volume":"volume"}
        df = df.rename(columns=ren)
        if "ticker" not in df.columns or df["ticker"].isna().any():
            name = p.name
            if name.endswith("_1d.parquet"):
                tk = name[:-len("_1d.parquet")].replace("_sa"," ").replace("_"," ").strip().replace(" ", "").upper()
            else:
                tk = name.upper()
            df["ticker"] = tk
        if "datetime_sp" in df.columns:
            s = pd.to_datetime(df["datetime_sp"], errors="coerce")
            df["date"] = pd.to_datetime(df.get("date", s), errors="coerce").dt.normalize()
        else:
            df["date"] = pd.to_datetime(df.get("date"), errors="coerce").dt.normalize()
        keep = ["ticker","date",metric]
        for c in keep:
            if c not in df.columns:
                df[c] = pd.NA
        all_rows.append(df[keep])
    tidy = pd.concat(all_rows, ignore_index=True)
    tidy = tidy.drop_duplicates(subset=["ticker","date"]).sort_values(["date","ticker"]) 
    panel = tidy.pivot(index="date", columns="ticker", values=metric).sort_index().reset_index()
    source = "from_02_adequado"

    panel.to_parquet(out_parquet, index=False, engine="pyarrow", compression="snappy")
    meta = {
        "path": str(out_parquet),
        "rows": int(panel.shape[0]),
        "cols": int(panel.shape[1]),
        "date_min": None if panel.empty else str(pd.to_datetime(panel["date"]).min().date()),
        "date_max": None if panel.empty else str(pd.to_datetime(panel["date"]).max().date()),
        "tickers": [] if panel.empty else [c for c in panel.columns if c != "date"],
        "source": source,
    }
    with open(out_manifest, "w", encoding="utf-8") as f:
        import json
        json.dump(meta, f, ensure_ascii=False, indent=2)
    print(f"SSOT {metric} ->", out_parquet, "| rows=", meta["rows"], "cols=", meta["cols"])
    return out_parquet


def most_recent_sp_date() -> date:
    now_sp = datetime.now(TZ_SP)
    return now_sp.date()


def main(argv: Optional[Iterable[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="Atualiza RAW -> 02_adequado -> SSOT (close/volume)")
    ap.add_argument("--start", help="Data inicial (YYYY-MM-DD) para ingestão total; default=incremental a partir do último arquivo", default=None)
    ap.add_argument("--end", help="Data final (YYYY-MM-DD); default=hoje em SP", default=None)
    ap.add_argument("--skip-ingest", action="store_true", help="Pula ingestão RAW")
    ap.add_argument("--skip-adequado", action="store_true", help="Pula construção 02_adequado")
    ap.add_argument("--skip-ssot", action="store_true", help="Pula construção SSOT")
    ap.add_argument("--floor", default="2012-01-01", help="Piso da janela caso ingestão completa seja necessária (YYYY-MM-DD)")
    args = ap.parse_args(list(argv) if argv is not None else None)

    root = project_root()
    raw_dir, adequado_dir, curado_dir, stage_dir = detect_dirs(root)

    floor_date = datetime.fromisoformat(args.floor).date()
    end_date = datetime.fromisoformat(args.end).date() if args.end else most_recent_sp_date()

    print("ROOT:", root)
    print("DIRS:", "raw=", raw_dir, "adequado=", adequado_dir, "curado=", curado_dir, "stage=", stage_dir)
    print("FIM janela:", end_date)

    if not args.skip_ingest:
        # Ingestão incremental por símbolo
        step_ingest_raw(raw_dir, floor_date, end_date)
    else:
        print("[skip] ingest raw")

    if not args.skip_adequado:
        step_build_adequado(raw_dir, adequado_dir)
    else:
        print("[skip] adequado")

    if not args.skip_ssot:
        build_ssot_from_adequado("close", adequado_dir, curado_dir)
        build_ssot_from_adequado("volume", adequado_dir, curado_dir)
    else:
        print("[skip] ssot")

    print("Concluído.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
