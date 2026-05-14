# Old Approach — Mouse & Keyboard Control

## What the plan was
Use pyautogui to control mouse and keyboard, feed screenshots 
to a local vision model, and navigate TradingView to scrape 
options prices visually.

## Why this approach was scrapped
- Local vision models are unreliable for reading precise financial numbers
- UI-based scraping breaks when layouts change or popups appear
- Screenshot → model → action loop is too slow and stateless

## What replaced it
Moved to API-based data fetching (yfinance / Tradier) with 
Playwright for any browser navigation needed. Local model 
is used as a judge, not a driver.

Progress shall continue