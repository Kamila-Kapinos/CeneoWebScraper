from __future__ import print_function
import json
import os
from turtle import pen
import requests
import pandas as pd
from bs4 import BeautifulSoup
from app.services.OpinionsService import OpinionsService
from app.services.ProductsService import ProductsService
from app.utils import get_item
from app.models.opinion import Opinion
from matplotlib import pyplot as plt

plt.switch_backend('Agg') 

class Product:
    def __init__(self, product_id=0, opinions=None, product_name="", opinions_count=0, pros_count=0, cons_count=0, average_score=0):
        self.product_id = product_id
        self.product_name = product_name
        if opinions: 
            self.opinions = opinions
        else:
            self.opinions = []
        self.opinions_count = opinions_count
        self.pros_count = pros_count
        self.cons_count = cons_count
        self.average_score = average_score
    
    def __str__(self):
        return f"""product_id: {self.product_id}<br>
        product_name: {self.product_name}<br>
        opinions_count: {self.opinions_count}<br>
        pros_count: {self.pros_count}<br>
        cons_count: {self.cons_count}<br>
        average_score: {self.average_score}<br>
        opinions: <br><br>
        """ + "<br><br>".join(str(opinion) for opinion in self.opinions)

    def __repr__(self):
        return f"Product(product_id={self.product_id}, product_name={self.product_name}, opinions_count={self.opinions_count}, pros_count={self.pros_count}, cons_count={self.cons_count}, average_score={self.average_score}, opinions: [" + ", ".join(opinion.__repr__() for opinion in self.opinions) + "])"

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "product_name": self.product_name,
            "opinions_count": self.opinions_count,
            "pros_count": self.pros_count,
            "cons_count": self.cons_count,
            "average_score": self.average_score,
            "opinions": [opinion.to_dict() for opinion in self.opinions]
        }

    def stats_to_dict(self):
        return {
            "product_id": self.product_id,
            "product_name": self.product_name,
            "opinions_count": self.opinions_count,
            "pros_count": self.pros_count,
            "cons_count": self.cons_count,
            "average_score": self.average_score
        }
    def stats_labels(self):
            return {
            "product_id": "ID Produktu",
            "product_name": "Nazwa Produktu",
            "opinions_count": "Liczba Opinii",
            "pros_count": "Liczba Zalet",
            "cons_count": "Liczba Wad",
            "average_score": "Średnia liczba gwiazdek"
        }
    
    def opinions_to_dict(self):
        return [opinion.to_dict() for opinion in self.opinions]

    def extract_product(self):
        url = f"https://www.ceneo.pl/{self.product_id}#tab=reviews"
        response = requests.get(url)

        f = open('app/logs/product_' + self.product_id + '.html', "a")
        f.write(response.text)
        f.close()

        page = BeautifulSoup(response.text, 'html.parser')

        self.product_name = get_item(page, "h1.product-top__product-info__name")

        if not self.product_name:
            raise Exception("No product exist")

        db_obj = ProductsService().get_product(self.product_id)
        if not db_obj:
            ProductsService().add_product(self)

        while(url):
            response = requests.get(url)
            page = BeautifulSoup(response.text, 'html.parser')
            opinions = page.select("div.js_product-review")
            for opinion in opinions:
                self.opinions.append(Opinion().extract_opinion(opinion))
            try:    
                url = "https://www.ceneo.pl"+get_item(page,"a.pagination__next","href")
            except TypeError:
                url = None

        return self
    
    def opinions_to_df(self):
        opinions = pd.DataFrame([opinion.to_dict() for opinion in self.opinions])
        if not opinions.empty:
            opinions.stars = opinions.stars.map(lambda x: float(x.split("/")[0].replace(",", ".")))
        return opinions
    
    def process_stats(self):
        df = self.opinions_to_df()
        if not df.empty:
            self.opinions_count = df.shape[0]
            self.pros_count = df.pros.map(bool).sum()
            self.cons_count = df.cons.map(bool).sum()
            self.average_score = df.stars.mean().round(2)
        return self

    def draw_charts(self): 
        df = self.opinions_to_df()
        if not df.empty:
            recommendation = df.recommendation.value_counts(dropna = False).sort_index().reindex(["Nie polecam", "Polecam", None])
            recommendation.plot.pie(
                label="", 
                autopct="%1.1f%%", 
                colors=["lightsalmon", "lightgreen", "lightskyblue"],
                labels=["Nie polecam", "Polecam", "Nie mam zdania"]
            )
            plt.title("Rekomendacja")
            plt.savefig(f"app/static/plots/{self.product_id}_recommendations.png")
            plt.close()
            stars = df.stars.value_counts().sort_index().reindex([x / 10.0 for x in range(5, 51, 5)], fill_value=0)
            stars.plot.bar()
            plt.title("Oceny produktu")
            plt.xlabel("Liczba gwiazdek")
            plt.ylabel("Liczba opinii")
            plt.grid(True)
            plt.xticks(rotation=0)
            plt.savefig(f"app/static/plots/{self.product_id}_stars.png")
            plt.close()

    def save_opinions(self):
        if self.product_name:
            OpinionsService().clear_product_opinions(self.product_id)
            for opinion in self.opinions:
                OpinionsService().add_product_opinion(self.product_id, opinion)
            if not os.path.exists("app/opinions"):
                os.makedirs("app/opinions")
            with open(f"app/opinions/{self.product_id}.json", "w", encoding="UTF-8") as jf:
                json.dump(self.opinions_to_dict(), jf, indent=4, ensure_ascii=False)
            
    
    def save_stats(self):
        print('save_stats', self.product_name)   
        if self.product_name:
            ProductsService().update_product(self)
              
    def load_product(self):
        product = ProductsService().get_product(self.product_id)
        self.product_id = product["id"]
        self.product_name = product["name"]
        self.opinions_count = product["opinions_count"]
        self.pros_count = product["pros_count"]
        self.cons_count = product["cons_count"]
        self.average_score = product["average_score"]

        opinions = OpinionsService().get_product_opinions(self.product_id)
        for opinion in opinions:
            print(opinion)
            pros = self.parseArrayFromString(opinion['pros'])
            cons = self.parseArrayFromString(opinion['cons'])
            self.opinions.append(
                Opinion(opinion['author'], opinion['recommendation'], opinion['stars'], opinion['content'], opinion['useful'], 
                opinion['useless'], opinion['publish_date'], opinion['purchase_date'], pros, cons, opinion['opinion_id'])
                )

    def parseArrayFromString(self, str):
        if str == '[]':
            return []
        elif str[0] == '[':
            return str[2:-2].split("', '")
        else:
            return []    