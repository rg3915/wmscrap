clean:
	@find . -name "*.pyc" | xargs rm -rf
	@find . -name "*.pyo" | xargs rm -rf
	@find . -name "__pycache__" -type d | xargs rm -rf
	@find . -name "*.csv" -type f | xargs rm -rf
	@find . -name "*.json" -type f | xargs rm -rf
	@find . -name "*.log" -type f | xargs rm -rf

run: clean
	scrapy crawl webmotors
	
install:
	pip install -r requirements.txt