clean:
	@find . -name "*.pyc" | xargs rm -rf
	@find . -name "*.pyo" | xargs rm -rf
	@find . -name "__pycache__" -type d | xargs rm -rf
	@find . -name "*.csv" -type f | xargs rm -rf
	@find . -name "*.json" -type f | xargs rm -rf
	@find . -name "*.log" -type f | xargs rm -rf

run: clean
	redis-server &
	scrapy crawl webmotors -a force_last_page=$(PAGES) --logfile=webmotors.log
	
install:
	pip install -r requirements.txt