class opml:
    lines = []
    XML = ""
    data = {}

    def __init__(self):
        self.lines.append('<?xml version="1.0" encoding="UTF-8"?>')
        self.lines.append('<opml version="1.0">')
        self.lines.append('<head><title>Title</title></head>')
    # 初始化

    def addItem(self, title, url, cate="def"):
        if cate not in self.data:
            self.data[cate] = []
        self.data[cate].append({"title": title, "url": url})
    # 添加订阅源条目

    def buildCate(self, cate):
        for item in self.data[cate]:
            self.lines.append('<outline text="%s" title="%s">' % (cate, cate))
            self.buildItem(item)
            self.lines.append('</outline>')
    # 按分类构建内容

    def buildItem(self, item):
        self.lines.append('<outline type="rss" text="%s" title="%s" xmlUrl="%s" />' %
                          (item["title"], item["title"], item["url"]))
    # 按分类构建内容

    def buildBody(self):
        self.lines.append('<body>')
        for cate in self.data:
            self.buildCate(cate)
        self.lines.append('</body>')
        self.lines.append('</opml>')
        self.XML = self.XML.join(self.lines)
    # 生成 body

    def outPut(self):
        self.buildBody()
        print(self.XML)
    # 输出

    def saveToFile(self, file):
        if not any(self.XML):
            self.buildBody()
        with open(file, 'w', encoding='utf-8', newline="\n") as f:
            f.write(self.XML)
    # 输出
