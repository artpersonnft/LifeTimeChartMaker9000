import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import plotly.graph_objects as go
from datetime import datetime
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor
import numpy as np

# Function to download and process data for a single ticker (CPU-only)
def download_ticker(args):
    ticker, start_date, end_date = args  # Unpack the arguments
    try:
        print(f"Downloading data for {ticker}...")
        stock = yf.Ticker(ticker)
        data = stock.history(start=start_date, end=end_date)
        if not data.empty:
            # Calculate percentage increase on CPU using Pandas/NumPy
            initial_price = data["Close"].iloc[0]
            percentage_data = ((data["Close"] - initial_price) / initial_price) * 100
            percentage_data.name = "Percentage"  # Name the Series for clarity
            raw_price_data = data["Close"]
            start_date = data.index[0]
            print(f"Data for {ticker} starts from {start_date.strftime('%Y-%m-%d')}")
            return ticker, percentage_data, raw_price_data, start_date
        else:
            print(f"No data available for {ticker}")
            return ticker, None, None, None
    except Exception as e:
        print(f"Error downloading {ticker}: {e}")
        return ticker, None, None, None

# Main script
if __name__ == "__main__":
    # Prompt for tickers with validation
    def get_tickers_from_input():
        while True:
            user_input = input("Input Tickers (comma-separated, 1-5 letters each, no suffix, or press Enter for default): ").strip()
            
            # If the user presses Enter (empty input), return the default ticker list
            if not user_input:
                return [
                    "AADR", "AAIT", "AAVX", "AAXJ", "ABCS", "ACCU", "ACIM", "ACWI", "ACWV", "ACWX",
                    "ADRA", "ADRD", "ADRE", "ADRU", "ADZ", "AFK", "AGA", "AGEM", "AGF", "AGG",
                    "AGLS", "AGND", "AGOL", "AGQ", "AGRG", "AGZ", "AGZD", "AIA", "ALD", "ALFA",
                    "ALT", "ALTL", "ALUM", "AMJ", "AMLP", "AMPS", "AMU", "AND", "ANGL", "AOA",
                    "AOK", "AOM", "AOR", "ARGT", "ASDR", "ASEA", "ASHR", "ASO", "ATMP", "AUD",
                    "AUNZ", "AUSE", "AXDI", "AXEN", "AXFN", "AXHE", "AXID", "AXIT", "AXJL",
                    "AXJS", "AXMT", "AXSL", "AXTE", "AXUT", "AYT", "AZIA", "BAB", "BABS",
                    "BABZ", "BAL", "BARL", "BARN", "BBH", "BBRC", "BBVX", "BCM", "BDCL", "BDCS",
                    "BDD", "BDG", "BDH", "BFOR", "BGU", "BGZ", "BHH", "BIB", "BICK", "BIK",
                    "BIL", "BIS", "BIV", "BIZD", "BJK", "BKF", "BKLN", "BLND", "BLNG", "BLV",
                    "BND", "BNDX", "BNO", "BNPC", "BNZ", "BOIL", "BOM", "BOND", "BONO", "BOS",
                    "BRAF", "BRAQ", "BRAZ", "BRF", "BRIL", "BRIS", "BRXX", "BRZS", "BRZU", "BSC",
                    "BSCB", "BSCC", "BSCD", "BSCE", "BSCF", "BSCG", "BSCH", "BSCI", "BSCJ",
                    "BSCK", "BSCL", "BSCM", "BSJC", "BSJD", "BSJE", "BSJF", "BSJG", "BSJH",
                    "BSJI", "BSJJ", "BSJK", "BSR", "BSV", "BTAH", "BTAL", "BUND", "BUNL", "BUNT",
                    "BVL", "BVT", "BWV", "BWX", "BWZ", "BXDB", "BXDC", "BXDD", "BXUB", "BXUC",
                    "BZF", "BZQ", "CAD", "CAFE", "CANE", "CAPE", "CARZ", "CBND", "CCVX", "CCX",
                    "CCXE", "CEFL", "CEMB", "CEW", "CFT", "CGW", "CHEP", "CHIB", "CHIE", "CHII",
                    "CHIM", "CHIQ", "CHIX", "CHLC", "CHNA", "CHOC", "CHXF", "CHXX", "CIU", "CLY",
                    "CMBS", "CMD", "CMF", "CNDA", "CNPF", "CNTR", "CNY", "COBO", "COLX", "CONG",
                    "COPX", "CORN", "CORP", "COW", "COWL", "COWS", "CPER", "CPI", "CQQQ", "CRBA",
                    "CRBI", "CRBQ", "CRO", "CROC", "CROP", "CRUD", "CSCB", "CSCR", "CSD", "CSJ",
                    "CSLS", "CSM", "CSMA", "CSMB", "CSMN", "CTNN", "CU", "CUPM", "CURE", "CUT",
                    "CVOL", "CVRT", "CVY", "CWB", "CWI", "CXA", "CYB", "CZA", "CZI", "CZM",
                    "DAG", "DBA", "DBAP", "DBB", "DBBR", "DBC", "DBCN", "DBE", "DBEF", "DBEM",
                    "DBEU", "DBGR", "DBIZ", "DBJP", "DBN", "DBO", "DBP", "DBR", "DBS", "DBT",
                    "DBU", "DBUK", "DBV", "DCNG", "DDG", "DDI", "DDM", "DDP", "DDVX", "DEB",
                    "DEE", "DEF", "DEFL", "DEM", "DENT", "DES", "DEW", "DFE", "DFJ", "DFVL",
                    "DFVS", "DGAZ", "DGG", "DGL", "DGLD", "DGP", "DGRE", "DGRS", "DGRW", "DGS",
                    "DGT", "DGZ", "DHS", "DIA", "DIG", "DIM", "DIRT", "DIV", "DIVS", "DJCI",
                    "DJP", "DKA", "DLBL", "DLBS", "DLN", "DLS", "DMM", "DND", "DNH", "DNL",
                    "DNO", "DOD", "DOG", "DOIL", "DOL", "DON", "DOO", "DOY", "DPC", "DPK",
                    "DPN", "DPU", "DRF", "DRGS", "DRN", "DRR", "DRV", "DRW", "DSC", "DSG",
                    "DSI", "DSLV", "DSTJ", "DSUM", "DSV", "DSXJ", "DTD", "DTH", "DTN", "DTO",
                    "DUG", "DVY", "DWM", "DWX", "DXD", "DXJ", "DXO", "DYY", "DZK", "DZZ",
                    "EAPS", "EATX", "EBND", "ECH", "ECNS", "ECON", "EDC", "EDEN", "EDIV", "EDV",
                    "EDZ", "EEB", "EEG", "EEH", "EEHB", "EELV", "EEM", "EEME", "EEML", "EEMS",
                    "EEMV", "EEN", "EEO", "EES", "EET", "EEV", "EEVX", "EEZ", "EFA", "EFAV",
                    "EFG", "EFN", "EFNL", "EFO", "EFU", "EFV", "EFZ", "EGPT", "EGRW", "EIDO",
                    "EIPL", "EIPO", "EIRL", "EIS", "EKH", "ELD", "ELG", "ELR", "ELV", "EMAG",
                    "EMB", "EMBB", "EMCB", "EMCD", "EMCG", "EMCR", "EMDD", "EMDG", "EMDI",
                    "EMDR", "EMER", "EMEY", "EMFM", "EMFN", "EMFT", "EMG", "EMGX", "EMHD",
                    "EMHY", "EMIF", "EMLB", "EMLC", "EMLP", "EMM", "EMMT", "EMSA", "EMT", "EMV",
                    "EMVX", "ENFR", "ENGN", "ENOR", "ENY", "ENZL", "EPHE", "EPI", "EPOL", "EPP",
                    "EPS", "EPU", "EPV", "EQIN", "EQL", "ERO", "ERUS", "ERW", "ERX", "ERY",
                    "ESR", "ETFY", "EU", "EUFN", "EUM", "EUO", "EUSA", "EVX", "EWA", "EWC",
                    "EWD", "EWG", "EWH", "EWI", "EWJ", "EWK", "EWL", "EWM", "EWN", "EWO", "EWP",
                    "EWQ", "EWS", "EWT", "EWU", "EWV", "EWW", "EWX", "EWY", "EWZ", "EXB", "EXI",
                    "EXT", "EZA", "EZJ", "EZM", "EZU", "EZY", "FAA", "FAB", "FAD", "FAN", "FAS",
                    "FAUS", "FAZ", "FBM", "FBT", "FBZ", "FCA", "FCAN", "FCD", "FCG", "FCGL",
                    "FCGS", "FCHI", "FCL", "FCOM", "FCQ", "FCV", "FDD", "FDIS", "FDL", "FDM",
                    "FDN", "FDT", "FDTS", "FDV", "FEEU", "FEFN", "FEG", "FEM", "FEMS", "FENY",
                    "FEP", "FEU", "FEX", "FEZ", "FFL", "FFR", "FFVX", "FGD", "FGEM", "FGHY",
                    "FGM", "FHC", "FHK", "FHLC", "FIDU", "FIGY", "FIL", "FILL", "FINF", "FINU",
                    "FINZ", "FIO", "FISN", "FIVZ", "FIW", "FJP", "FKL", "FKO", "FKU", "FLAG",
                    "FLAT", "FLG", "FLM", "FLN", "FLOT", "FLRN", "FLTR", "FLYX", "FM", "FMAT",
                    "FMF", "FMK", "FMM", "FMU", "FMV", "FNCL", "FNDA", "FNDB", "FNDC", "FNDE",
                    "FNDF", "FNDX", "FNI", "FNIO", "FNK", "FNX", "FNY", "FOC", "FOIL", "FOL",
                    "FONE", "FORX", "FOS", "FPA", "FPE", "FPX", "FRI", "FRN", "FTA", "FTC",
                    "FTY", "FUD", "FUE", "FVD", "FVI", "FVL", "FXA", "FXB", "FXC", "FXD", "FXE",
                    "FXF", "FXG", "FXH", "FXI", "FXL", "FXM", "FXN", "FXO", "FXP", "FXR", "FXS",
                    "FXU", "FXY", "FXZ", "FYX", "FZB", "GAF", "GAL", "GASL", "GASX", "GASZ",
                    "GAZ", "GBB", "GBF", "GCC", "GCE", "GDAY", "GDX", "GDXJ", "GEMS", "GERJ",
                    "GEX", "GGEM", "GGGG", "GGOV", "GHYG", "GII", "GIVE", "GIY", "GLCB", "GLD",
                    "GLDI", "GLDX", "GLJ", "GLL", "GLTR", "GMF", "GMFS", "GML", "GMM", "GMMB",
                    "GMTB", "GNAT", "GNMA", "GNR", "GOE", "GOVT", "GQRE", "GREK", "GRES", "GRI",
                    "GRID", "GRN", "GRPC", "GRU", "GRV", "GRWN", "GSAX", "GSC", "GSD", "GSG",
                    "GSGO", "GSMA", "GSO", "GSP", "GSR", "GSRA", "GSW", "GSY", "GSZ", "GTAA",
                    "GTIP", "GULF", "GUNR", "GUR", "GURU", "GVI", "GVT", "GWL", "GWO", "GWX",
                    "GXC", "GXF", "GXG", "GYLD", "HAO", "HAP", "HBTA", "HDG", "HDGE", "HDGI",
                    "HDIV", "HDV", "HECO", "HEDJ", "HEVY", "HFIN", "HGEM", "HGI", "HHH", "HILO",
                    "HKK", "HMTM", "HPVW", "HSPX", "HUSE", "HVOL", "HVPW", "HYD", "HYE", "HYEM",
                    "HYG", "HYHG", "HYLD", "HYLS", "HYMB", "HYND", "HYS", "HYXU", "HYZD", "IAH",
                    "IAI", "IAK", "IAT", "IAU", "IBB", "IBCB", "IBCC", "IBCD", "IBCE", "IBDA",
                    "IBDB", "IBDC", "IBDD", "IBND", "ICF", "ICI", "ICLN", "ICN", "ICOL", "IDHB",
                    "IDHQ", "IDLV", "IDOG", "IDU", "IDV", "IDX", "IDXJ", "IEF", "IEFA", "IEI",
                    "IELG", "IEMG", "IEO", "IESM", "IEV", "IEZ", "IFAS", "IFEU", "IFGL", "IFNA",
                    "IFSM", "IGE", "IGEM", "IGF", "IGHG", "IGM", "IGN", "IGOV", "IGS", "IGU",
                    "IGV", "IGW", "IHE", "IHF", "IHI", "IHY", "IIH", "IJH", "IJJ", "IJK", "IJR",
                    "IJS", "IJT", "ILB", "ILF", "ILTB", "IMLP", "INCO", "INDA", "INDL", "INDY",
                    "INDZ", "INFL", "INKM", "INP", "INR", "INSD", "INXX", "INY", "IOIL", "IOO",
                    "IPAL", "IPD", "IPE", "IPF", "IPFF", "IPK", "IPLT", "IPN", "IPO", "IPS",
                    "IPU", "IPW", "IQDE", "IQDF", "IQDY", "IRO", "IRV", "IRY", "ISHG", "ISI",
                    "IST", "ITA", "ITB", "ITE", "ITF", "ITM", "ITR", "IVE", "IVV", "IVW", "IWB",
                    "IWC", "IWD", "IWF", "IWL", "IWM", "IWN", "IWO", "IWP", "IWR", "IWS", "IWV",
                    "IWW", "IWX", "IWY", "IWZ", "IXC", "IXG", "IXJ", "IXN", "IXP", "IYC", "IYE",
                    "IYF", "IYG", "IYH", "IYJ", "IYK", "IYM", "IYR", "IYT", "IYW", "IYY", "IYZ",
                    "JCO", "JDST", "JEM", "JFT", "JGBB", "JGBD", "JGBL", "JGBS", "JGBT", "JJA",
                    "JJAC", "JJC", "JJE", "JJG", "JJM", "JJN", "JJP", "JJS", "JJT", "JJU", "JKD",
                    "JKE", "JKF", "JKG", "JKH", "JKI", "JKJ", "JKK", "JKL", "JNK", "JO", "JPNL",
                    "JPNS", "JPP", "JPX", "JSC", "JUNR", "JVS", "JXI", "JYF", "JYN", "KBE",
                    "KBWB", "KBWC", "KBWD", "KBWI", "KBWP", "KBWR", "KBWX", "KBWY", "KCE",
                    "KFYP", "KIE", "KLD", "KME", "KNOW", "KOL", "KOLD", "KORU", "KORZ", "KRE",
                    "KROO", "KRS", "KRU", "KWT", "KXI", "LAG", "LATM", "LBJ", "LBND", "LBTA",
                    "LCPR", "LD", "LEDD", "LEMB", "LGEM", "LGLV", "LHB", "LIT", "LPAL", "LPLT",
                    "LQD", "LSC", "LSKY", "LSO", "LSTK", "LTL", "LTPZ", "LVL", "LVOL", "LWC",
                    "LWPE", "MATH", "MATL", "MATS", "MBB", "MBG", "MCHI", "MCRO", "MDD", "MDIV",
                    "MDY", "MDYG", "MDYV", "MES", "MEXS", "MFLA", "MFSA", "MGC", "MGK", "MGV",
                    "MIDU", "MIDZ", "MINC", "MINT", "MKH", "MLN", "MLPA", "MLPC", "MLPG", "MLPI",
                    "MLPJ", "MLPL", "MLPN", "MLPS", "MLPW", "MLPX", "MLPY", "MMTM", "MNA",
                    "MOAT", "MOM", "MONY", "MOO", "MORL", "MORT", "MRGR", "MSXX", "MTK", "MTUM",
                    "MUAA", "MUAB", "MUAC", "MUAD", "MUAE", "MUAF", "MUB", "MUNI", "MVV", "MWJ",
                    "MWN", "MXI", "MYY", "MZG", "MZN", "MZO", "MZZ", "NAGS", "NASH", "NASI",
                    "NFO", "NFRA", "NGE", "NIB", "NINI", "NKY", "NLR", "NOBL", "NOMO", "NORW",
                    "NUCL", "NY", "NYC", "NYF", "OEF", "OFF", "OGEM", "OIH", "OIL", "OILZ",
                    "OLEM", "OLO", "ONEF", "ONEQ", "ONG", "ONN", "OOK", "OTP", "OTR", "PAF",
                    "PAGG", "PALL", "PAO", "PBD", "PBE", "PBJ", "PBP", "PBS", "PBTQ", "PBW",
                    "PCA", "PCEF", "PCY", "PDN", "PDP", "PEF", "PEJ", "PEK", "PERM", "PEX",
                    "PEY", "PEZ", "PFA", "PFEM", "PFF", "PFI", "PFIG", "PFM", "PFXF", "PGAL",
                    "PGD", "PGF", "PGHY", "PGJ", "PGM", "PGX", "PHB", "PHDG", "PHO", "PHYS",
                    "PIC", "PICB", "PICK", "PID", "PIE", "PIN", "PIO", "PIQ", "PIV", "PIZ",
                    "PJB", "PJF", "PJG", "PJM", "PJO", "PJP", "PKB", "PKN", "PKOL", "PKW", "PLK",
                    "PLND", "PLTM", "PLW", "PMA", "PMNA", "PMR", "PMY", "PNQI", "PNXQ", "PPA",
                    "PPH", "PPLT", "PQBW", "PQSC", "PQY", "PQZ", "PRB", "PRF", "PRFZ", "PRN",
                    "PSAU", "PSCC", "PSCD", "PSCE", "PSCF", "PSCH", "PSCI", "PSCM", "PSCT",
                    "PSCU", "PSI", "PSJ", "PSK", "PSL", "PSP", "PSQ", "PSR", "PST", "PSTL",
                    "PTD", "PTE", "PTF", "PTH", "PTJ", "PTM", "PTO", "PTRP", "PUI", "PUW",
                    "PVI", "PWB", "PWC", "PWJ", "PWND", "PWO", "PWP", "PWT", "PWV", "PWY",
                    "PWZ", "PXE", "PXF", "PXH", "PXI", "PXJ", "PXN", "PXQ", "PXR", "PYH", "PYZ",
                    "PZA", "PZD", "PZI", "PZJ", "PZT", "QABA", "QAI", "QCLN", "QDEF", "QDF",
                    "QDYN", "QEH", "QGEM", "QID", "QLD", "QLT", "QLTA", "QLTB", "QLTC", "QMN",
                    "QQEW", "QQQ", "QQQC", "QQQE", "QQQM", "QQQQ", "QQQV", "QQXT", "QTEC",
                    "QUAL", "RALS", "RAVI", "RBL", "RCD", "RDIV", "REA", "REC", "REK", "REM",
                    "REMX", "RETL", "RETS", "REW", "REZ", "RFF", "RFG", "RFL", "RFN", "RFV",
                    "RGI", "RGRA", "RGRC", "RGRE", "RGRI", "RGRP", "RHM", "RHO", "RHS", "RIGS",
                    "RINF", "RING", "RJA", "RJI", "RJN", "RJZ", "RKH", "RLY", "RMB", "RMM",
                    "RMS", "ROB", "ROBO", "ROI", "ROLA", "ROM", "ROOF", "ROSA", "RPG", "RPQ",
                    "RPV", "RPX", "RRF", "RRGR", "RRY", "RRZ", "RSP", "RSU", "RSUN", "RSW",
                    "RSX", "RSXJ", "RTG", "RTH", "RTL", "RTLA", "RTM", "RTR", "RTSA", "RTW",
                    "RUDR", "RUSL", "RUSS", "RVNU", "RWG", "RWJ", "RWK", "RWL", "RWM", "RWO",
                    "RWR", "RWV", "RWW", "RWX", "RWXL", "RXD", "RXI", "RXL", "RYE", "RYF",
                    "RYH", "RYJ", "RYT", "RYU", "RZG", "RZV", "SAA", "SAGG", "SBB", "SBM",
                    "SBND", "SBV", "SCC", "SCEQ", "SCHA", "SCHB", "SCHC", "SCHD", "SCHE",
                    "SCHF", "SCHG", "SCHH", "SCHM", "SCHO", "SCHP", "SCHR", "SCHV", "SCHX",
                    "SCHZ", "SCIF", "SCIN", "SCJ", "SCLP", "SCO", "SCOG", "SCPB", "SCPR", "SCTR",
                    "SCZ", "SDD", "SDK", "SDIV", "SDOG", "SDOW", "SDP", "SDS", "SDY", "SDYL",
                    "SEA", "SEF", "SFK", "SFLA", "SFSA", "SGAR", "SGG", "SGGG", "SGOL", "SH",
                    "SHBT", "SHM", "SHMO", "SHV", "SHVY", "SHY", "SHYG", "SICK", "SIJ", "SIL",
                    "SILJ", "SINF", "SIVR", "SIZ", "SIZE", "SJB", "SJF", "SJH", "SJL", "SJNK",
                    "SKF", "SKK", "SKOR", "SKYY", "SLBT", "SLQD", "SLV", "SLVO", "SLVP", "SLVY",
                    "SLX", "SLY", "SLYG", "SLYV", "SMB", "SMDD", "SMDV", "SMH", "SMIN", "SMK",
                    "SMLV", "SMMU", "SMN", "SNDS", "SNLN", "SOCL", "SOIL", "SOXL", "SOXS",
                    "SPGH", "SPXU", "SPY", "SQQQ", "SRS", "SRTY", "SSG", "SSO", "STH", "STPZ",
                    "SUB", "SWH", "SZK", "SZO", "SZR", "TAGS", "TAN", "TAO", "TBAR", "TBF",
                    "TBT", "TBX", "TBZ", "TCHI", "TDD", "TDH", "TDIV", "TDN", "TDTF", "TDTS",
                    "TDTT", "TDV", "TDX", "TECL", "TECS", "TENZ", "TEST", "TFI", "TGEM", "TGR",
                    "THD", "THHY", "TILT", "TIP", "TIPX", "TIPZ", "TLH", "TLL", "TLO", "TLT",
                    "TLTD", "TLTE", "TMF", "TMV", "TMW", "TNA", "TNDQ", "TOK", "TOTS", "TPS",
                    "TQQQ", "TRND", "TRNM", "TRSK", "TRSY", "TRXT", "TSXV", "TTFS", "TTH", "TTT",
                    "TUR", "TUZ", "TVIX", "TVIZ", "TWM", "TWOK", "TWOL", "TWON", "TWOZ", "TWQ",
                    "TWTI", "TXF", "TYBS", "TYD", "TYH", "TYNS", "TYO", "TYP", "TZA", "TZD",
                    "TZE", "TZG", "TZI", "TZL", "TZO", "TZV", "TZW", "TZY", "UAG", "UBC", "UBD",
                    "UBG", "UBM", "UBN", "UBR", "UBT", "UCC", "UCD", "UCI", "UCO", "UDN", "UDNT",
                    "UDOW", "UEM", "UGA", "UGAZ", "UGE", "UGEM", "UGL", "UGLD", "UHN", "UINF",
                    "UJB", "UKF", "UKK", "UKW", "ULE", "ULQ", "ULST", "UMDD", "UMM", "UMX",
                    "UNG", "UNL", "UOIL", "UOY", "UPRO", "UPV", "UPW", "URA", "URE", "URR",
                    "URTH", "URTY", "USAG", "USCI", "USD", "USDU", "USL", "USLV", "USMI", "USMV",
                    "USO", "UST", "USV", "USY", "UTH", "UTLT", "UUP", "UUPT", "UVG", "UVT",
                    "UVU", "UVXY", "UWC", "UWM", "UWTI", "UXI", "UXJ", "UYG", "UYM", "VAW", "VB",
                    "VBK", "VBR", "VCIT", "VCLT", "VCR", "VCSH", "VDC", "VDE", "VEA", "VEGA",
                    "VEGI", "VEU", "VFH", "VGEM", "VGIT", "VGK", "VGLT", "VGSH", "VGT", "VHT",
                    "VIDI", "VIG", "VIIX", "VIIZ", "VIOG", "VIOO", "VIOV", "VIS", "VIXH", "VIXM",
                    "VIXY", "VLAT", "VLU", "VLUE", "VMBS", "VNM", "VNQ", "VNQI", "VO", "VOE",
                    "VONE", "VONG", "VONV", "VOO", "VOOG", "VOOV", "VOT", "VOX", "VPL", "VPU",
                    "VQT", "VRD", "VROM", "VSPR", "VSPY", "VSS", "VT", "VTHR", "VTI", "VTIP",
                    "VTV", "VTWG", "VTWO", "VTWV", "VUG", "VV", "VWO", "VWOB", "VXAA", "VXBB",
                    "VXCC", "VXDD", "VXEE", "VXF", "VXFF", "VXUS", "VXX", "VXZ", "VYM", "VZZ",
                    "VZZB", "WCAT", "WDIV", "WDTI", "WEAT", "WEET", "WFVK", "WIP", "WITE",
                    "WMCR", "WMH", "WMW", "WOOD", "WPS", "WREI", "WSTE", "WXSP", "XAR", "XBI",
                    "XES", "XGC", "XHB", "XHE", "XHMO", "XHS", "XIV", "XLB", "XLBS", "XLBT",
                    "XLE", "XLES", "XLF", "XLFS", "XLG", "XLI", "XLIS", "XLK", "XLKS", "XLP",
                    "XLPS", "XLU", "XLUS", "XLV", "XLVO", "XLVS", "XLY", "XLYS", "XME", "XMLV",
                    "XMPT", "XOIL", "XOP", "XOVR", "XPH", "XPP", "XRO", "XRT", "XRU", "XSD",
                    "XSLV", "XSW", "XTL", "XTN", "XVIX", "XVZ", "XXV", "YANG", "YAO", "YCL",
                    "YCS", "YDIV", "YINN", "YMLI", "YMLP", "YXI", "YYY", "ZIV", "ZROZ", "ZSL"
                ], False #False indicates default was used
            
            # Split the input by commas and clean up each ticker
            ticker_list = [ticker.strip().upper() for ticker in user_input.split(",")]
            
            # Validate each ticker
            valid = True
            for ticker in ticker_list:
                # Check length (1 to 5 characters)
                if not (1 <= len(ticker) <= 5):
                    print(f"Error: Ticker '{ticker}' must be 1 to 5 letters long.")
                    valid = False
                    break
                # Check if ticker contains only letters (no suffixes or special characters)
                if not ticker.isalpha():
                    print(f"Error: Ticker '{ticker}' must contain only letters (no suffixes like '.TO' or special characters).")
                    valid = False
                    break
            
            if valid:
                return ticker_list, True  # True indicates user provided input
            else:
                print("Please try again.")

    # Get the tickers (either from user input or default)
    tickers, user_provided_input = get_tickers_from_input()
    if user_provided_input:
        print(f"Using tickers: {tickers}")

    # Set date range
    end_date = datetime.now().strftime('%Y-%m-%d')
    stock_data = {}
    raw_data = {}
    start_dates = {}
    earliest_date = None

    # Prepare arguments for each ticker
    ticker_args = [(ticker, "1900-01-01", end_date) for ticker in tickers]

    # Use ProcessPoolExecutor to parallelize data downloading
    with ProcessPoolExecutor(max_workers=mp.cpu_count()) as executor:
        # Map the download function to all tickers
        results = executor.map(download_ticker, ticker_args)

        # Process results
        for ticker, percentage_data, raw_price_data, start_date in results:
            if percentage_data is not None:
                stock_data[ticker] = percentage_data
                raw_data[ticker] = raw_price_data
                start_dates[ticker] = start_date
                if earliest_date is None or start_date < earliest_date:
                    earliest_date = start_date

    if not stock_data:
        print("No data available for any ticker.")
        exit()

    # User input for chart option
    while True:
        print("\nChoose a charting option:")
        print("1: Group by 5-year buckets from the earliest date")
        print("2: Group by majority start dates (10+ tickers per date)")
        print("3: Chart all tickers in one chart")
        print("4: Chart tickers in partitions of 100 (with price or percentage option)")
        option = input("Enter 1, 2, 3, or 4: ").strip()
        
        if option in ["1", "2", "3", "4"]:
            break
        else:
            print("Invalid option selected. Please enter 1, 2, 3, or 4.")

    if option == "1":
        # Option 1: 5-year buckets
        buckets = {}
        for ticker, start_date in start_dates.items():
            years_since_earliest = (start_date - earliest_date).days / 365.25
            bucket = int(years_since_earliest // 5) * 5
            if bucket not in buckets:
                buckets[bucket] = []
            buckets[bucket].append(ticker)

        for bucket_start, ticker_list in sorted(buckets.items()):
            bucket_end = bucket_start + 5
            plt.figure(figsize=(16, 9), dpi=240)
            for ticker in ticker_list:
                plt.plot(stock_data[ticker].index, stock_data[ticker], label=ticker)
            
            plt.title(f"Percentage Increase (Start: {bucket_start}-{bucket_end} Years After {earliest_date.strftime('%Y-%m-%d')})")
            plt.xlabel("Date")
            plt.ylabel("Percentage Increase (%)")
            plt.legend()
            plt.grid(True)
            plt.xticks(rotation=45)
            
            filename = f"chart_{bucket_start}_to_{bucket_end}_years.png"
            plt.tight_layout()
            plt.savefig(filename)
            print(f"Saved chart: {filename}")
            plt.close()

    elif option == "2":
        # Option 2: Group by majority start dates (10+ tickers)
        date_counts = Counter(start_dates.values())
        majority_dates = [date for date, count in date_counts.items() if count >= 10]
        majority_dates.sort()

        if not majority_dates:
            print("No dates found with 10 or more tickers starting.")
        else:
            for i, start_date in enumerate(majority_dates):
                ticker_list = [ticker for ticker, date in start_dates.items() if date == start_date]
                plt.figure(figsize=(16, 9), dpi=240)
                for ticker in ticker_list:
                    plt.plot(stock_data[ticker].index, stock_data[ticker], label=ticker)
                
                plt.title(f"Percentage Increase (Start Date: {start_date.strftime('%Y-%m-%d')})")
                plt.xlabel("Date")
                plt.ylabel("Percentage Increase (%)")
                plt.legend()
                plt.grid(True)
                plt.xticks(rotation=45)
                
                filename = f"chart_start_{start_date.strftime('%Y-%m-%d')}.png"
                plt.tight_layout()
                plt.savefig(filename)
                print(f"Saved chart: {filename}")
                plt.close()

    elif option == "3":
        # Option 3: All tickers in one chart
        plt.figure(figsize=(16, 9), dpi=480)
        for ticker in stock_data:
            plt.plot(stock_data[ticker].index, stock_data[ticker], label=ticker)
        
        plt.title("Percentage Increase - All Tickers")
        plt.xlabel("Date")
        plt.ylabel("Percentage Increase (%)")
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)
        
        filename = "chart_all_tickers_percentage.png"
        plt.tight_layout()
        plt.savefig(filename)
        print(f"Saved chart: {filename}")
        plt.close()

        # Interactive Plotly chart for raw prices
        fig = go.Figure()
        for ticker in raw_data:
            fig.add_trace(go.Scatter(
                x=raw_data[ticker].index,
                y=raw_data[ticker],
                name=ticker,
                mode='lines',
                hovertemplate=f"{ticker}<br>Date: %{{x}}<br>Price: %{{y:.2f}} USD"
            ))

        fig.update_layout(
            title="Stock Prices Over Time",
            xaxis_title="Date",
            yaxis_title="Price (USD)",
            legend_title="Tickers",
            hovermode="x unified",
            template="plotly_white",
            width=2560,
            height=1440
        )

        fig.show()

    elif option == "4":
        # Option 4: Chart tickers in partitions of 100 with price or percentage option
        while True:
            metric_choice = input("Display y-axis as (P)rice or (P)ercentage? Enter P or %: ").strip().upper()
            if metric_choice in ["P", "%"]:
                break
            else:
                print("Invalid choice. Please enter 'P' for Price or '%' for Percentage.")

        batch_size = 100
        ticker_list = list(raw_data.keys())
        for i in range(0, len(ticker_list), batch_size):
            batch_tickers = ticker_list[i:i + batch_size]
            fig = go.Figure()
            
            if metric_choice == "P":
                for ticker in batch_tickers:
                    fig.add_trace(go.Scatter(
                        x=raw_data[ticker].index,
                        y=raw_data[ticker],
                        name=ticker,
                        mode='lines',
                        hovertemplate=f"{ticker}<br>Date: %{{x}}<br>Price: %{{y:.2f}} USD"
                    ))
                y_axis_title = "Price (USD)"
                chart_title = f"Stock Prices Over Time (Tickers {i+1} to {i+len(batch_tickers)})"
            else:
                for ticker in batch_tickers:
                    fig.add_trace(go.Scatter(
                        x=stock_data[ticker].index,
                        y=stock_data[ticker],
                        name=ticker,
                        mode='lines',
                        hovertemplate=f"{ticker}<br>Date: %{{x}}<br>Percentage: %{{y:.2f}}%"
                    ))
                y_axis_title = "Percentage Increase (%)"
                chart_title = f"Percentage Increase Over Time (Tickers {i+1} to {i+len(batch_tickers)})"

            fig.update_layout(
                title=chart_title,
                xaxis_title="Date",
                yaxis_title=y_axis_title,
                legend_title="Tickers",
                hovermode="closest",
                template="plotly_white",
                width=2560,
                height=1440
            )

            fig.show()

    print("Chart generation complete.")
