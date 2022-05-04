# Used-Car-Price-History-Tool  
Purpose/Goal:  
  -Periodically gather used vehicle data from online car dealerships and displays the price history of a searched vehicle in the user GUI.  
  -Wanted to experiment and learn more about web scraping, handle large amounts of data entries, develop my skills in Python, and learn tkinter.  
  
TODOs:  
  -Automate the web scraping process  
  -Add more scrapers for other websites  
  -Finish AutoNation scraper  
  -Possibly move away from saving data to csv files since they can grow to be very large  
  -Improve/fix bugs in GUI
  -MP scraper fix  
  
Usage:  
  -Run Carvana_Scraper_Multiprocessing.py to gather data (this will have to be done daily/weekly/etc. to build up data).  
  -Run Merge_To_DF.py to combine all produced csv files into 1 main csv file.  
  -Run UserGUI.py to display price history graph. Requires a mainy_df.csv to work.  
  -Use mainy_df.csv in repository to test UserGUI.py with some sample data collected over a couple weeks.  
