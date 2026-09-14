from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from datetime import datetime
from zoneinfo import ZoneInfo
import google_sheets
import time

URLS = [
    "https://chartink.com/screener/fut-sreelakshmi-guruvayoorappan-b-atr-volume-rocket",
    "https://chartink.com/screener/copy-copy-copy-future-and-option-pin-bar-pranshu-tiwari-2",
    "https://chartink.com/screener/copy-copy-how-to-find-future-and-option-stocks-buy-entry-future-3",
    "https://chartink.com/screener/copy-copy-nks-future-trick-bb-part-2-21",
    "https://chartink.com/screener/copy-copy-nks-future-trick-bb-part-2-20",
    "https://chartink.com/screener/fut-hammar-cash-low-paradaily",
    "https://chartink.com/screener/copy-bullish-kicker-with-momentum-btst-futures-99",
    "https://chartink.com/screener/copy-bearish-kicker-with-momentum-stbt-futures-58",
    "https://chartink.com/screener/sncopy-shani-crow-future",
    "https://chartink.com/screener/copy-shani-crow-future-2",
    "https://chartink.com/screener/copy-copy-copy-copy-merge-nk-daily-convergence-future-nk-sir-hm-positional-buy-nk-sir-4796",
    "https://chartink.com/screener/tcssjbl1fut-rocket",
    "https://chartink.com/screener/copy-narayana-futures-positional-bearish-111",
    "https://chartink.com/screener/new-11111sjbl1fut-rocket",
    "https://chartink.com/screener/copy-love-future",
    "https://chartink.com/screener/tnsjbl5fut-bulloong-4",
    "https://chartink.com/screener/copy-sjbl5fut-bulloong-4",
    "https://chartink.com/screener/11111sjbl1fut-rocket",
    "https://chartink.com/screener/copy-sjbl1fut-rocket-2",
    "https://chartink.com/screener/copy-the-best-btst-193",
    "https://chartink.com/screener/22-nw-shesha-magic-buy-love",
    "https://chartink.com/screener/all-u1-nk-sir-s-uptrend-stocks-all-time-uptrend",
    "https://chartink.com/screener/copy-sjbl6ch-shesha-buy-bollinger-band-weekly",
    "https://chartink.com/screener/copy-copy-bb-blaster-2",
    "https://chartink.com/screener/copy-atr-volume-f-o-200-wkly-rsi-70-16",
    "https://chartink.com/screener/copy-copy-copy-explosive-move-day-coming-in-1-2-days",
    "https://chartink.com/screener/50-sreelakshmi-guruvayoorappan-b-atr-volume-rocket",
    "https://chartink.com/screener/50agp-bullish2-p5",
    "https://chartink.com/screener/50aaa13-vp-sheshapathi"
]
 

sheet_id = "1DUXCEmDDIS-2ONCyAaq74bJ31jUKtD7n5pocccGNvMo"
worksheet_names = ["p1","p2","p3","p4","p5","p6","p7","p8","p9","p10","p11","p12","p13","p14","p15","p16","p17","p18","p19","p20","p21","p22","p23","p24","p25","p26","p27","p28","p29"]

def scrape_chartink(url, worksheet_name):
    print(f"\n🚀 Starting scrape for '{worksheet_name}'")
    print(f"🌐 Loading URL: {url}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        headers = ["Sr", "Stock Name", "Symbol", "Close", "Change", "Price", "Volume"]

        try:
            page.goto(url, wait_until="domcontentloaded")
            time.sleep(1)

            if page.is_visible("text='No records found'"):
                print(f"⚠️ No records found at {url}. Writing 'No Data'.")
                rows = [[""]]
            else:
                try:
                    page.wait_for_selector(
                        "tbody tr",
                        timeout=10000
                    )
                    
                    table_rows = page.query_selector_all(
                        "tbody tr"
                    )

                    print(f"📥 Extracted {len(table_rows)} rows.")

                    rows = []

                    for row in table_rows:
                    
                        sr = row.query_selector(
                            'td[data-field="sr"]'
                        )
                    
                        stock = row.query_selector(
                            'td[data-field="name"]'
                        )
                    
                        symbol = row.query_selector(
                            'td[data-field="nsecode"]'
                        )
                    
                        close = row.query_selector(
                            'td[data-field="scan-column-default-close"]'
                        )
                    
                        change = row.query_selector(
                            'td[data-field="scan-column-default-percent-change"]'
                        )
                    
                        volume = row.query_selector(
                            'td[data-field="scan-column-default-volume"]'
                        )
                    
                        rows.append([
                            sr.text_content().strip() if sr else "",
                            stock.text_content().strip() if stock else "",
                            symbol.text_content().strip() if symbol else "",
                            close.text_content().strip() if close else "",
                            change.text_content().strip() if change else "",
                            volume.text_content().strip() if volume else ""
                        ])

                    if len(rows) == 0:
                        print("⚠️ Table found but no rows present. Writing 'No Data'.")
                        rows = [[""]]

                except PlaywrightTimeoutError:
                    print(f"❌ Table not found at {url}. Writing 'No Data'.")
                    rows = [[""]]
           
            google_sheets.update_google_sheet_by_name(
                sheet_id, worksheet_name, headers, rows
            )

        except PlaywrightTimeoutError:
            print(f"❌ Timeout error at {url}. Writing 'No Data'.")
            google_sheets.update_google_sheet_by_name(
                sheet_id, worksheet_name, headers, [[""]]
            )

        except Exception as e:
            print(f"❌ Unexpected error: {e}. Writing 'No Data'.")
            google_sheets.update_google_sheet_by_name(
                sheet_id, worksheet_name, headers, [[""]]
            )

        finally:
            browser.close()

        now = datetime.now(
            ZoneInfo("Asia/Kolkata")
        ).strftime(
            "Last updated: %d-%m-%Y %H:%M:%S IST"
        )
        google_sheets.append_footer(sheet_id, worksheet_name, [now])

        print(f"✅ Worksheet '{worksheet_name}' update finished.")

for index, url in enumerate(URLS):
    scrape_chartink(url, worksheet_names[index])
    print(f"⏱️ Finished updating '{worksheet_names[index]}'")
