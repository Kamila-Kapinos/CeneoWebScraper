class Opinion():
    def __init__(self, opinion_id, author, recommendation, stars, content, useful, useless, publish_date, purchase_date, pros, cons):
        self.opinion_id = opinion_id
        self.author = author
        self.recommendation = recommendation
        self.stars = stars
        self.content = content
        self.useful = useful
        self.useless = useless
        self.publish_date = publish_date
        self.purchase_date = purchase_date
        self.pros = pros
        self.cons = cons