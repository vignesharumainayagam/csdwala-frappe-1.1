from __future__ import unicode_literals
import frappe, os

from frappe.website.utils import can_cache, delete_page_cache, extract_title
from frappe.model.document import get_controller
from six import text_type
import io


class CustomURL(object):
    def __init__(self):
        self.IsCustom = None

    def getCustomUrl(self):
    	return self.custom_url

    def setCustomPage(self,page):
	    	self.IsCustom = True  
	    	self.custom_url =  page


    def setCustomUrl(self,path):

    	self.url=path.split('/')[0].lower()
    	self.url_length =len(path.split('/'))


    	if(self.url_length == 1):
    		self.getsingledata(path)

    	if(self.url_length == 2):
    		self.gettwodata(path) 

     	if(self.url_length == 3):
    		self.getthirddata(path)

     	if(self.url_length == 4):
    		self.getfourdata(path)




    def getsingledata(self,path):
    	self.routes = self.check_routes(path,['Custom Page','Category'])
    	if(self.routes.get('doctype') == 'Custom Page' and self.routes.get("route") == path ):
    		self.setCustomPage('custompage')

    	if(self.routes.get('doctype') == 'Category' and self.routes.get("route") == path ):
    		self.setCustomPage('cathomepage')


    	if(len(path.split('/')[0].split('-'))>1):
	    	self.ItemBrand = self.check_routes(path.split('/')[0].split('-')[0],['ItemBrand'])
	    	self.Category = self.check_routes(path.split('/')[0].split('-')[1],['Category'])
	    	if(self.Category.get('doctype') == 'Category' and self.Category.get("route") == path.split('/')[0].split('-')[1] and self.ItemBrand.get('doctype') == 'ItemBrand' and self.ItemBrand.get("route") == path.split('/')[0].split('-')[0]  ):
	    		self.setCustomPage('listpage')


    def gettwodata(self,path):
    	dealerpath = path.split('/')
    	self.routes = self.check_routes(dealerpath[1],['Dealers','News'])
    	if(self.routes.get('doctype') == 'Dealers' and dealerpath[0] == 'dealers' and self.routes.get("route") == dealerpath[1] ):
    		self.setCustomPage('dealers')

        if(self.routes.get('doctype') == 'News' and dealerpath[0] == 'news' and self.routes.get("route") == dealerpath[1] ):
            self.setCustomPage('blog_detail')

    	if(len(path.split('/')[0].split('-'))>1):
	    	self.ItemBrand = self.check_routes(path.split('/')[0].split('-')[0],['ItemBrand'])
	    	self.Category = self.check_routes(path.split('/')[0].split('-')[1],['Category'])
    		self.routes = self.check_routes(path.split('/')[1],['Item'])

	    	if( self.routes.get('doctype') == 'Item'  and self.routes.get("route") == path.split('/')[1] and  self.Category.get('doctype') == 'Category' and self.Category.get("route") == path.split('/')[0].split('-')[1] and self.ItemBrand.get('doctype') == 'ItemBrand' and self.ItemBrand.get("route") == path.split('/')[0].split('-')[0]  ):
	    		self.setCustomPage('detailpage')

    def getthirddata(self,path):
    	dealerpath = path.split('/')
    	self.routes = self.check_routes(dealerpath[1],['Dealers'])
    	if(self.routes.get('doctype') == 'Dealers' and dealerpath[0] == 'dealers' and self.routes.get("route") == dealerpath[1] ):
    		self.setCustomPage('dealers')
    	if(len(path.split('/')[0].split('-'))>1):
	    	self.ItemBrand = self.check_routes(path.split('/')[0].split('-')[0],['ItemBrand'])
	    	self.Category = self.check_routes(path.split('/')[0].split('-')[1],['Category'])
    		self.routes = self.check_routes(path.split('/')[1],['Item'])
    		self.Variant = self.check_routes(path.split('/')[2],['Item Variant'])

	    	if( self.Variant.get('doctype') == 'Item Variant'  and self.Variant.get("route") == path.split('/')[2] and self.routes.get('doctype') == 'Item'  and self.routes.get("route") == path.split('/')[1] and  self.Category.get('doctype') == 'Category' and self.Category.get("route") == path.split('/')[0].split('-')[1] and self.ItemBrand.get('doctype') == 'ItemBrand' and self.ItemBrand.get("route") == path.split('/')[0].split('-')[0]  ):
	    		self.setCustomPage('varientdetailpage')
	    	if( path.split('/')[2] == 'images' and self.routes.get('doctype') == 'Item'  and self.routes.get("route") == path.split('/')[1] and  self.Category.get('doctype') == 'Category' and self.Category.get("route") == path.split('/')[0].split('-')[1] and self.ItemBrand.get('doctype') == 'ItemBrand' and self.ItemBrand.get("route") == path.split('/')[0].split('-')[0]  ):
	    		self.setCustomPage('view_images')
	    	if( path.split('/')[2] == 'dealers' and self.routes.get('doctype') == 'Item'  and self.routes.get("route") == path.split('/')[1] and  self.Category.get('doctype') == 'Category' and self.Category.get("route") == path.split('/')[0].split('-')[1] and self.ItemBrand.get('doctype') == 'ItemBrand' and self.ItemBrand.get("route") == path.split('/')[0].split('-')[0]  ):
	    		self.setCustomPage('dealers_list')



    def getfourdata(self,path):
    	dealerpath = path.split('/')
    	self.routes = self.check_routes(dealerpath[1],['Dealers'])
    	if(self.routes.get('doctype') == 'Dealers' and dealerpath[0] == 'dealers' and self.routes.get("route") == dealerpath[1] ):
    		self.setCustomPage('dealers')
    	if(len(path.split('/')[0].split('-'))>1):
	    	self.ItemBrand = self.check_routes(path.split('/')[0].split('-')[0],['ItemBrand'])
	    	self.Category = self.check_routes(path.split('/')[0].split('-')[1],['Category'])
    		self.routes = self.check_routes(path.split('/')[1],['Item'])
    		self.Variant = self.check_routes(path.split('/')[2],['Item Variant'])

	    	if( path.split('/')[3] == 'images' and self.Variant.get('doctype') == 'Item Variant'  and self.Variant.get("route") == path.split('/')[2] and self.routes.get('doctype') == 'Item'  and self.routes.get("route") == path.split('/')[1] and  self.Category.get('doctype') == 'Category' and self.Category.get("route") == path.split('/')[0].split('-')[1] and self.ItemBrand.get('doctype') == 'ItemBrand' and self.ItemBrand.get("route") == path.split('/')[0].split('-')[0]  ):
	    		self.setCustomPage('view_images')


    def check_routes(self,path=None,doctypes=None):
		routes = {}
		for doctype in doctypes:
			values = []
			condition = ""
			if path:
				condition += ' {0} `route`=%s limit 1'.format('and' if 'where' in condition else 'where')
				values.append(path)
			try:
				for r in frappe.db.sql("""select route, name from `tab{0}` {1}""".format(doctype,condition), values=values, as_dict=True):
					routes[r.route] = {"doctype":doctype,"route": r.route}
					if path:
						return routes[r.route]
			except Exception as e:
				if e.args[0]!=1054: raise e
		return routes
