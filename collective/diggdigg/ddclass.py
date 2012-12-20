from urllib import quote
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm


VOTE_URL = 'VOTE_URL'
VOTE_TITLE = 'VOTE_TITLE'
VOTE_IMAGE = 'VOTE_IMAGE'
VOTE_BUTTON_DESIGN = 'VOTE_BUTTON_DESIGN'
VOTE_SOURCE = "VOTE_SOURCE"
SCHEDULER_TIMER = 'SCHEDULER_TIMER'
POST_ID = 'POST_ID'
VOTE_BUTTON_DESIGN_LAZY_WIDTH = 'VOTE_BUTTON_DESIGN_LAZY_WIDTH'
VOTE_BUTTON_DESIGN_LAZY_HEIGHT = 'VOTE_BUTTON_DESIGN_LAZY_HEIGHT'

# default value
DEFAULT_APPEND_TYPE = 'none'
DEFAULT_OPTION_AJAX = 'False'
DEFAULT_BUTTON_DESIGN = 'Normal'
DEFAULT_BUTTON_WEIGHT = '100'


class BaseDD(object):

    name = ""  # name of the vote button
    websiteURL = ""  # website URL
    apiURL = ""  # Button API for development

    baseURL = ""  # vote button URL, before construt
    baseURL_lazy = ""  # vote button URL, before construt, lazy version
    baseURL_lazy_script = ""  # jQuery script , lazy version
    scheduler_lazy_script = ""  # scheduler function
    scheduler_lazy_timer = ""  # miliseconds

    finalURL = ""  # final URL for display, after constructs
    finalURL_lazy = ""  # final lazy URL for display, after constructs
    finalURL_lazy_script = ""  # final jQuery, after constructs
    final_scheduler_lazy_script = ""  # final scheduler, after constructs

    isEncodeRequired = True
    islazyLoadAvailable = True  # is lazy load avaliable?

    # contains DD option value, in array
    wp_options = ""
    option_append_type = ""
    option_button_design = ""
    option_button_weight = ""
    option_ajax_left_float = ""
    option_lazy_load = ""

    button_weight_value = ""

    # default float button design
    float_button_design = DEFAULT_BUTTON_DESIGN

    # default button layout, suit in most cases
    buttonLayout = {"Normal": "Normal",
                        "Compact": "Compact"}

    #  Default options
    append_type = 'none'
    button_design = 'Normal'
    ajax_left_float = False
    lazy_load = False

    buttonLayoutLazy = {"Normal": "Normal", "Compact": "Compact"}
    buttonLayoutLazyWidth = {"Normal": "51", "Compact": "120"}
    buttonLayoutLazyHeight = {"Normal": "69", "Compact": "22"}

    def __init__(self, name, websiteURL, apiURL, baseURL):
        self.name = name
        self.websiteURL = websiteURL
        self.apiURL = apiURL
        self.baseURL = baseURL
        self.options = {}
        self.option_append_type = self.OPTION_APPEND_TYPE
        self.option_button_design = self.OPTION_BUTTON_DESIGN
        self.option_button_weight = self.OPTION_BUTTON_WEIGHT
        self.option_ajax_left_float = self.OPTION_AJAX_LEFT_FLOAT
        self.option_lazy_load = self.OPTION_LAZY_LOAD
        self.button_weight_value = self.DEFAULT_BUTTON_WEIGHT
        self.init_options()
        self.context = None
        self.request = None

    def init_options(self):
        self.options[self.option_append_type] = self.append_type
        self.options[self.option_button_design] = self.button_design
        self.options[self.option_ajax_left_float] = self.ajax_left_float
        self.options[self.option_lazy_load] = self.lazy_load
        self.options[self.option_button_weight] = self.button_weight_value

    def getButtonDesign(self, button):
        return self.buttonLayout[button]

    def getButtonDesignLazy(self, button):
        return self.buttonLayoutLazy[button]

    def getOptionLazyLoad(self):
        return self.options[self.option_lazy_load]

    def getOptionAjaxLeftFloat(self):
        return self.options[self.option_ajax_left_float]

    def getOptionButtonWeight(self):
        return self.options[self.option_button_weight]

    def getOptionAppendType(self):
        return self.options[self.option_append_type]

    def getOptionButtonDesign(self):
        return self.options[self.option_button_design]

    def constructURL(self, url, title, button, postId, lazy, globalcfg=''):
        #quote - replace space with %20
        #urlencode - replace space with +
        if(self.isEncodeRequired):
            title = quote(title)
            url = quote(url)

        if not lazy:
            self.constructNormalURL(url, title, button, postId)
        else:
            self.constructLazyLoadURL(url, title, button, postId)

    def constructNormalURL(self, url, title, button, postId):

        finalURL = self.baseURL
        finalURL = finalURL.replace(VOTE_BUTTON_DESIGN,
                                    self.getButtonDesign(button))
        finalURL = finalURL.replace(VOTE_TITLE, title)
        finalURL = finalURL.replace(VOTE_URL, url)
        self.finalURL = finalURL

    def constructLazyLoadURL(self, url, title, button, postId):

        finalURL_lazy = self.baseURL_lazy
        finalURL_lazy = finalURL_lazy.replace(VOTE_BUTTON_DESIGN,
                                              self.getButtonDesignLazy(button))
        finalURL_lazy = finalURL_lazy.replace(VOTE_TITLE, title)
        finalURL_lazy = finalURL_lazy.replace(VOTE_URL, url)
        finalURL_lazy = finalURL_lazy.replace(POST_ID, postId)
        self.finalURL_lazy = finalURL_lazy

        lazy_script = self.baseURL_lazy_script
        lazy_script = lazy_script.replace(VOTE_BUTTON_DESIGN_LAZY_WIDTH,
                                      self.getButtonDesignLazyWidth(button))
        lazy_script = lazy_script.replace(VOTE_BUTTON_DESIGN_LAZY_HEIGHT,
                                      self.getButtonDesignLazyHeight(button))
        lazy_script = lazy_script.replace(VOTE_BUTTON_DESIGN,
                                      self.getButtonDesignLazy(button))
        lazy_script = lazy_script.replace(VOTE_TITLE, title)
        lazy_script = lazy_script.replace(VOTE_URL, url)
        lazy_script = lazy_script.replace(POST_ID, postId)
        self.finalURL_lazy_script = lazy_script

        #scheduler to run the lazy loading
        lazy_script = self.scheduler_lazy_script
        lazy_script = lazy_script.replace(SCHEDULER_TIMER,
                                          self.scheduler_lazy_timer)
        lazy_script = lazy_script.replace(POST_ID, postId)
        self.final_scheduler_lazy_script = lazy_script


class BaseIFrameDD (BaseDD):
    EXTRA_VALUE = "EXTRA_VALUE"

    buttonLayoutWidthHeight = {
        "Normal": """height="69" width="51" """,
        "Compact": """height="22" width="120" """
    }

    def getIframeWH(self, button):
        return self.buttonLayoutWidthHeight[button]

    def constructNormalURL(self, url, title, button, postId):

        finalURL = self.baseURL
        finalURL = finalURL.replace(VOTE_BUTTON_DESIGN,
                                    self.getButtonDesign(button))
        finalURL = finalURL.replace(VOTE_TITLE, title)
        finalURL = finalURL.replace(VOTE_URL, url)
        finalURL = finalURL.replace(POST_ID, postId)

        finalURL = finalURL.replace(self.EXTRA_VALUE,
                                    self.getIframeWH(button))
        self.finalURL = finalURL

    def constructLazyLoadURL(self, url, title, button, postId):

        finalURL_lazy = self.baseURL_lazy
        finalURL_lazy = finalURL_lazy.replace(POST_ID, postId)
        self.finalURL_lazy = finalURL_lazy

        lazy_script = self.baseURL_lazy_script
        lazy_script = lazy_script.replace(VOTE_BUTTON_DESIGN_LAZY_WIDTH,
                                      self.getButtonDesignLazyWidth(button))
        lazy_script = lazy_script.replace(VOTE_BUTTON_DESIGN_LAZY_HEIGHT,
                                      self.getButtonDesignLazyHeight(button))
        lazy_script = lazy_script.replace(VOTE_BUTTON_DESIGN,
                                      self.getButtonDesignLazy(button))
        lazy_script = lazy_script.replace(VOTE_TITLE, title)
        lazy_script = lazy_script.replace(VOTE_URL, url)
        lazy_script = lazy_script.replace(POST_ID, postId)
        self.finalURL_lazy_script = lazy_script

        lazy_script = self.scheduler_lazy_script
        lazy_script = lazy_script.replace(SCHEDULER_TIMER,
                                      self.scheduler_lazy_timer)
        lazy_script = lazy_script.replace(POST_ID, postId)
        self.final_scheduler_lazy_script = lazy_script


class DD_Twitter(BaseDD):
    append_type = 'left_float'
    button_design = 'Normal'
    ajax_left_float = 'on'
    lazy_load = False

    NAME = "Twitter"
    URL_WEBSITE = "http://www.twitter.com"
    URL_API = "http://twitter.com/goodies/tweetbutton"
    DEFAULT_BUTTON_WEIGHT = "110"

    BASEURL = """<a href="http://twitter.com/share" class="twitter-share-button" data-url="VOTE_URL" data-count="VOTE_BUTTON_DESIGN" data-text="VOTE_TITLE" data-via="VOTE_SOURCE" ></a><script type="text/javascript" src="http://platform.twitter.com/widgets.js"></script>"""

    OPTION_APPEND_TYPE = "dd_twitter_appendType"
    OPTION_BUTTON_DESIGN = "dd_twitter_buttonDesign"
    OPTION_BUTTON_WEIGHT = "dd_twitter_button_weight"
    OPTION_AJAX_LEFT_FLOAT = "dd_twitter_ajax_left_float"
    OPTION_LAZY_LOAD = "dd_twitter_lazy_load"

    BASEURL_LAZY = """<div class='dd-twitter-ajax-load dd-twitter-POST_ID'></div><a href="http://twitter.com/share" class="twitter-share-button" data-url="VOTE_URL" data-count="VOTE_BUTTON_DESIGN" data-text="VOTE_TITLE" data-via="VOTE_SOURCE" ></a>";"""
    BASEURL_LAZY_SCRIPT = """ function loadTwitter_POST_ID(){ jQuery(document).ready(function($) { $('.dd-twitter-POST_ID').remove();$.getScript('http://platform.twitter.com/widgets.js'); }); }"""
    SCHEDULER_LAZY_SCRIPT = """window.setTimeout('loadTwitter_POST_ID()',SCHEDULER_TIMER);"""
    SCHEDULER_LAZY_TIMER = "1000"

    buttonLayout = {
        "Normal": "vertical",
        "Compact": "horizontal"
    }

    buttonLayoutLazy = {
        "Normal": "vertical",
        "Compact": "horizontal"
    }

    isEncodeRequired = False

    VOTE_SOURCE = "VOTE_SOURCE"

    def __init__(self, context, request):
        BaseDD.__init__(self,
                        self.NAME,
                        self.URL_WEBSITE,
                        self.URL_API,
                        self.BASEURL)
        self.baseURL_lazy = self.BASEURL_LAZY
        self.baseURL_lazy_script = self.BASEURL_LAZY_SCRIPT
        self.scheduler_lazy_script = self.SCHEDULER_LAZY_SCRIPT
        self.scheduler_lazy_timer = self.SCHEDULER_LAZY_TIMER
        self.context = context
        self.request = request

    def constructURL(self, url, title, button, postId, lazy, globalcfg=''):
        if(self.isEncodeRequired):
            title = quote(title)
            url = quote(url)

        twitter_source = ''

        if not lazy:
            #format twitter source
            self.baseURL = self.baseURL.replace(VOTE_SOURCE,
                                                twitter_source)

            self.constructNormalURL(url, title, button, postId)
        else:
            #format twitter source
            self.baseURL_lazy = self.baseURL_lazy.replace(VOTE_SOURCE,
                                                          twitter_source)

            self.constructLazyLoadURL(url, title, button, postId)

    def constructLazyLoadURL(self, url, title, button, postId):

        finalURL_lazy = self.baseURL_lazy
        finalURL_lazy = finalURL_lazy.replace(VOTE_BUTTON_DESIGN,
                                              self.getButtonDesignLazy(button))
        finalURL_lazy = finalURL_lazy.replace(VOTE_TITLE, title)
        finalURL_lazy = finalURL_lazy.replace(VOTE_URL, url)
        finalURL_lazy = finalURL_lazy.replace(POST_ID, postId)
        self.finalURL_lazy = finalURL_lazy

        lazy_script = self.baseURL_lazy_script
        lazy_script = lazy_script.replace(POST_ID, postId)
        self.finalURL_lazy_script = lazy_script

        lazy_script = self.scheduler_lazy_script
        lazy_script = lazy_script.replace(SCHEDULER_TIMER,
                                          self.scheduler_lazy_timer)
        lazy_script = lazy_script.replace(POST_ID, postId)
        self.final_scheduler_lazy_script = lazy_script

"""
class DD_Buffer (BaseDD):
    append_type = 'after_content'
    button_design = 'Normal'
    ajax_left_float = 'on'
    lazy_load = False
    
    NAME = "Buffer"
    URL_WEBSITE = "http:#bufferapp.com/"
    URL_API = "http:#bufferapp.com/goodies/button/"
    DEFAULT_BUTTON_WEIGHT = "99"
    
    isEncodeRequired = False
    
    BASEURL = '<a href="http:#bufferapp.com/add" class="buffer-add-button" data-count="VOTE_BUTTON_DESIGN" data-url="VOTE_URL" data-via="VOTE_BUFFER_SOURCE"></a><script type="text/javascript" src="http:#static.bufferapp.com/js/button.js"></script>'

    BASEURL_LAZY = '<a href="http:#bufferapp.com/add" class="buffer-add-button" data-count="VOTE_BUTTON_DESIGN" data-url="VOTE_URL" data-via="VOTE_BUFFER_SOURCE"></a>'
    BASEURL_LAZY_SCRIPT = "function loadBuffer_POST_ID(): jQuery(document).ready(function(\) { \('.dd-buffer-POST_ID').remove()\.getScript('http:#static.bufferapp.com/js/button.js') }) }"
    SCHEDULER_LAZY_SCRIPT = "window.setTimeout('loadBuffer_POST_ID()',SCHEDULER_TIMER)"
    SCHEDULER_LAZY_TIMER = "1000"
    
    OPTION_APPEND_TYPE = "dd_buffer_appendType"
    OPTION_BUTTON_DESIGN = "dd_buffer_buttonDesign"
    OPTION_BUTTON_WEIGHT = "dd_buffer_button_weight"
    OPTION_AJAX_LEFT_FLOAT = "dd_buffer_ajax_left_float"
    OPTION_LAZY_LOAD = "dd_buffer_lazy_load"
    
    VOTE_BUFFER_SOURCE = "VOTE_BUFFER_SOURCE"
    
    buttonLayout = {
        "Normal" : "vertical",
        "Compact" : "horizontal",
        "No Count" : "none"
    )
    
    buttonLayoutLazy = {
        "Normal" : "vertical",
        "Compact" : "horizontal",
        "No Count" : "none"
    )
    
    # XXX: Old-style constructor
    def DD_Buffer() {
        
        self.option_append_type = self.OPTION_APPEND_TYPE
        self.option_button_design = self.OPTION_BUTTON_DESIGN
        self.option_button_weight = self.OPTION_BUTTON_WEIGHT
        self.option_ajax_left_float = self.OPTION_AJAX_LEFT_FLOAT
        self.option_lazy_load = self.OPTION_LAZY_LOAD
        
        self.baseURL_lazy = self.BASEURL_LAZY
        self.baseURL_lazy_script = self.BASEURL_LAZY_SCRIPT
        self.scheduler_lazy_script = self.SCHEDULER_LAZY_SCRIPT
        self.scheduler_lazy_timer = self.SCHEDULER_LAZY_TIMER
        
        self.button_weight_value = self.DEFAULT_BUTTON_WEIGHT
        
        self.BaseDD(self.NAME, self.URL_WEBSITE, self.URL_API, self.BASEURL)
      
    }

    def constructURL(url, title, button, postId, lazy, globalcfg = ''):
        
         if(self.isEncodeRequired):
             title = quote(title)
            url = quote(url)
         }
         
         buffer_source = ''
         if(globalcfg!=''):
             buffer_source = globalcfg[DD_GLOBAL_BUFFER_OPTION][DD_GLOBAL_BUFFER_OPTION_SOURCE]
         }

        if(lazy==DD_EMPTY_VALUE || lazy==False):
            #format twitter source
            self.baseURL = str_replace(VOTE_BUFFER_SOURCE,buffer_source,self.baseURL)
            self.constructNormalURL(url, title,button, postId)           
        }else{
            #format twitter source
            self.baseURL_lazy = str_replace(VOTE_BUFFER_SOURCE,buffer_source,self.baseURL_lazy)
        
            self.constructLazyLoadURL(url, title,button, postId)
        }
        
    }
    
    def constructNormalURL(url, title, button, postId):
        
        finalURL = self.baseURL
        finalURL = str_replace(VOTE_BUTTON_DESIGN,self.getButtonDesign(button),finalURL)
        finalURL = str_replace(VOTE_TITLE,title,finalURL)
        finalURL = str_replace(VOTE_URL,url,finalURL)
        finalURL = str_replace(POST_ID,postId,finalURL)
        self.finalURL = finalURL
    }

    def constructLazyLoadURL(url, title,button, postId):
        
        finalURL_lazy = self.baseURL_lazy
        finalURL_lazy = str_replace(VOTE_URL,url,finalURL_lazy)
        finalURL_lazy = str_replace(VOTE_BUTTON_DESIGN,self.getButtonDesignLazy(button),finalURL_lazy)
        finalURL_lazy = str_replace(POST_ID,postId,finalURL_lazy)
        self.finalURL_lazy = finalURL_lazy
        
        finalURL_lazy_script = self.baseURL_lazy_script
        finalURL_lazy_script = str_replace(POST_ID,postId,finalURL_lazy_script)
        self.finalURL_lazy_script = finalURL_lazy_script
        
        final_scheduler_lazy_script = self.scheduler_lazy_script
        final_scheduler_lazy_script = str_replace(SCHEDULER_TIMER,self.scheduler_lazy_timer,final_scheduler_lazy_script)
        final_scheduler_lazy_script = str_replace(POST_ID,postId,final_scheduler_lazy_script)
        self.final_scheduler_lazy_script =  final_scheduler_lazy_script
        
"""


class DD_FbLike_XFBML(BaseDD):
    append_type = 'left_float'
    button_design = 'Like Button Count'
    ajax_left_float = 'on'
    lazy_load = False

    NAME = "Facebook Like (XFBML)"
    URL_WEBSITE = "http:#www.facebook.com"
    URL_API = "http://developers.facebook.com/docs/reference/plugins/like"

    BASEURL = """<script src="http://connect.facebook.net/FACEBOOK_LOCALE/all.js#xfbml=1"></script><fb:like href="VOTE_URL" FACEBOOK_SEND FACEBOOK_SHOW_FACE VOTE_BUTTON_DESIGN ></fb:like>"""

    FB_LOCALES = "http://www.facebook.com/translations/FacebookLocales.xml"
    DEFAULT_BUTTON_WEIGHT = "96"

    OPTION_APPEND_TYPE = "dd_fblike_xfbml_appendType"
    OPTION_BUTTON_DESIGN = "dd_fblike_xfbml_buttonDesign"
    OPTION_BUTTON_WEIGHT = "dd_fblike_xfbml_button_weight"
    OPTION_AJAX_LEFT_FLOAT = "dd_fblike_xfbml_ajax_left_float"
    OPTION_LAZY_LOAD = "dd_fblike_xfbml_lazy_load"

    LIKE_STANDARD = """ width="450" """
    LIKE_BUTTON_COUNT = """ layout="button_count" width="92" """
    LIKE_BOX_COUNT = """ layout="box_count" width="50" """
    RECOMMEND_STANDARD = """ action="recommend" width="400" """
    RECOMMEND_BUTTON_COUNT = """ action="recommend" layout="button_count" width="130" """
    RECOMMEND_BOX_COUNT = """ action="recommend" layout="box_count" width="90" """

    FACEBOOK_SEND = "FACEBOOK_SEND"  # send="True"
    FACEBOOK_SHOW_FACE = "FACEBOOK_SHOW_FACE"  # show_faces="True" 
    FACEBOOK_LOCALE = "FACEBOOK_LOCALE"

    islazyLoadAvailable = False

    float_button_design = "Like Box Count"

    buttonLayout = {
        "Like Standard": LIKE_STANDARD,
        "Like Button Count": LIKE_BUTTON_COUNT,
        "Like Box Count": LIKE_BOX_COUNT,
        "Recommend Standard": RECOMMEND_STANDARD,
        "Recommend Button Count": RECOMMEND_BUTTON_COUNT,
        "Recommend Box Count": RECOMMEND_BOX_COUNT
    }

    def __init__(self, context, request):
        BaseDD.__init__(self, self.NAME, self.URL_WEBSITE, self.URL_API, self.BASEURL)

        self.context = context
        self.request = request

        self.option_append_type = self.OPTION_APPEND_TYPE
        self.option_button_design = self.OPTION_BUTTON_DESIGN
        self.option_button_weight = self.OPTION_BUTTON_WEIGHT
        self.option_ajax_left_float = self.OPTION_AJAX_LEFT_FLOAT
        self.option_lazy_load = self.OPTION_LAZY_LOAD

        self.button_weight_value = self.DEFAULT_BUTTON_WEIGHT

    def constructURL(self, url, title, button, postId, lazy, globalcfg=''):
        if(self.isEncodeRequired):
            title = quote(title)
            url = quote(url)

        fb_locale = 'en_US'
        fb_send = ''
        fb_face = ''
        fb_send_value = ''
        fb_face_value = ''

        if fb_send:
            fb_send_value = "send=\"true\""
        else:
            fb_send_value = "send=\"false\""

        if fb_face:
            fb_face_value = "show_faces=\"true\""
        else:
            fb_face_value = "show_faces=\"false\""

        #show face and send button 
        self.baseURL = self.baseURL.replace(self.FACEBOOK_LOCALE, fb_locale)
        self.baseURL = self.baseURL.replace(self.FACEBOOK_SEND, fb_send_value)
        self.baseURL = self.baseURL.replace(self.FACEBOOK_SHOW_FACE,
                                            fb_face_value)

        self.constructNormalURL(url, title, button, postId)

"""
/******************************************************************************************
 * 
 * http:#www.google.com/+1/button/
 * http:#www.google.com/webmasters/+1/button/
 *
 */
class DD_Google1 (BaseDD):
    append_type = 'left_float'
    button_design = 'Normal'
    ajax_left_float = 'on'
    lazy_load = False
    
    NAME = "Google +1"
    URL_WEBSITE = "http:#www.google.com/+1/button/"
    URL_API = "http:#code.google.com/apis/+1button/"
    DEFAULT_BUTTON_WEIGHT = "95"
    
    isEncodeRequired = False
    
    BASEURL = "<script type='text/javascript' src='https:#apis.google.com/js/plusone.js'></script><g:plusone size='VOTE_BUTTON_DESIGN' href='VOTE_URL'></g:plusone>"

    BASEURL_LAZY = "<div class='dd-google1-ajax-load dd-google1-POST_ID'></div><g:plusone size='VOTE_BUTTON_DESIGN' href='VOTE_URL'></g:plusone>"
    BASEURL_LAZY_SCRIPT = " function loadGoogle1_POST_ID(): jQuery(document).ready(function(\) { \('.dd-google1-POST_ID').remove()\.getScript('https:#apis.google.com/js/plusone.js') }) }"
    SCHEDULER_LAZY_SCRIPT = "window.setTimeout('loadGoogle1_POST_ID()',SCHEDULER_TIMER)"
    SCHEDULER_LAZY_TIMER = "1000"
    
    OPTION_APPEND_TYPE = "dd_google1_appendType"
    OPTION_BUTTON_DESIGN = "dd_google1_buttonDesign"
    OPTION_BUTTON_WEIGHT = "dd_google1_button_weight"
    OPTION_AJAX_LEFT_FLOAT = "dd_google1_ajax_left_float"
    OPTION_LAZY_LOAD = "dd_google1_lazy_load"
    
    buttonLayout = {
        "Normal" : "tall",
        "Compact (15px)" : "small",
        "Compact (20px)" : "medium",
        "Compact (24px)" : "none"
    )
    
    buttonLayoutLazy = {
        "Normal" : "tall",
        "Compact (15px)" : "small",
        "Compact (20px)" : "medium",
        "Compact (24px)" : "none"
    )
    
    def DD_Google1() {
        
        self.option_append_type = self.OPTION_APPEND_TYPE
        self.option_button_design = self.OPTION_BUTTON_DESIGN
        self.option_button_weight = self.OPTION_BUTTON_WEIGHT
        self.option_ajax_left_float = self.OPTION_AJAX_LEFT_FLOAT
        self.option_lazy_load = self.OPTION_LAZY_LOAD
        
        self.baseURL_lazy = self.BASEURL_LAZY
        self.baseURL_lazy_script = self.BASEURL_LAZY_SCRIPT
        self.scheduler_lazy_script = self.SCHEDULER_LAZY_SCRIPT
        self.scheduler_lazy_timer = self.SCHEDULER_LAZY_TIMER
        
        self.button_weight_value = self.DEFAULT_BUTTON_WEIGHT
        
        self.BaseDD(self.NAME, self.URL_WEBSITE, self.URL_API, self.BASEURL)
      
    }
    
    def constructLazyLoadURL(url, title,button, postId):
        
        finalURL_lazy = self.baseURL_lazy
        finalURL_lazy = str_replace(VOTE_URL,url,finalURL_lazy)
        finalURL_lazy = str_replace(VOTE_BUTTON_DESIGN,self.getButtonDesignLazy(button),finalURL_lazy)
        finalURL_lazy = str_replace(POST_ID,postId,finalURL_lazy)
        self.finalURL_lazy = finalURL_lazy
        
        finalURL_lazy_script = self.baseURL_lazy_script
        finalURL_lazy_script = str_replace(POST_ID,postId,finalURL_lazy_script)
        self.finalURL_lazy_script = finalURL_lazy_script
        
        final_scheduler_lazy_script = self.scheduler_lazy_script
        final_scheduler_lazy_script = str_replace(SCHEDULER_TIMER,self.scheduler_lazy_timer,final_scheduler_lazy_script)
        final_scheduler_lazy_script = str_replace(POST_ID,postId,final_scheduler_lazy_script)
        self.final_scheduler_lazy_script =  final_scheduler_lazy_script
        

/******************************************************************************************
 * 
 * http:#www.linkedin.com
 *
 */
class DD_Linkedin (BaseDD):
    append_type = 'left_float'
    button_design = 'Normal'
    ajax_left_float = 'on'
    lazy_load = False
    
    NAME = "Linkedin"
    URL_WEBSITE = "http:#www.linkedin.com"
    URL_API = "http:#www.linkedin.com/publishers"
    DEFAULT_BUTTON_WEIGHT = "94"
    
    BASEURL = "<script type='text/javascript' src='http:#platform.linkedin.com/in.js'></script><div class='dd-linkedin-share'><div data-url='VOTE_URL' data-counter='VOTE_BUTTON_DESIGN'></div></div>"
    
    BASEURL_LAZY = "<div class='dd-linkedin-ajax-load dd-linkedin-POST_ID'></div><script type='IN/share' data-url='VOTE_URL' data-counter='VOTE_BUTTON_DESIGN'></script>"
    BASEURL_LAZY_SCRIPT = " function loadLinkedin_POST_ID(): jQuery(document).ready(function(\) { \('.dd-linkedin-POST_ID').remove()\.getScript('http:#platform.linkedin.com/in.js') }) }"
    SCHEDULER_LAZY_SCRIPT = "window.setTimeout('loadLinkedin_POST_ID()',SCHEDULER_TIMER)"
    SCHEDULER_LAZY_TIMER = "1000"
    
    OPTION_APPEND_TYPE = "dd_linkedin_appendType"
    OPTION_BUTTON_DESIGN = "dd_linkedin_buttonDesign"
    OPTION_BUTTON_WEIGHT = "dd_linkedin_button_weight"
    OPTION_AJAX_LEFT_FLOAT = "dd_linkedin_ajax_left_float"
    OPTION_LAZY_LOAD = "dd_linkedin_lazy_load"

    buttonLayout = {
        "Normal" : "top",
        "Compact" : "right",
        "NoCount" : "none" 
    )
    
    buttonLayoutLazy = {
        "Normal" : "top",
        "Compact" : "right",
        "NoCount" : "none" 
    )
    
    isEncodeRequired = False
    
    def DD_Linkedin() {
        
        self.option_append_type = self.OPTION_APPEND_TYPE
        self.option_button_design = self.OPTION_BUTTON_DESIGN
        self.option_button_weight = self.OPTION_BUTTON_WEIGHT
        self.option_ajax_left_float = self.OPTION_AJAX_LEFT_FLOAT
        self.option_lazy_load = self.OPTION_LAZY_LOAD
        
        self.baseURL_lazy = self.BASEURL_LAZY
        self.baseURL_lazy_script = self.BASEURL_LAZY_SCRIPT
        self.scheduler_lazy_script = self.SCHEDULER_LAZY_SCRIPT
        self.scheduler_lazy_timer = self.SCHEDULER_LAZY_TIMER
        
        self.button_weight_value = self.DEFAULT_BUTTON_WEIGHT
        
        self.BaseDD(self.NAME, self.URL_WEBSITE, self.URL_API, self.BASEURL)
      
    } 
    
    def constructLazyLoadURL(url, title,button, postId):
        
        finalURL_lazy = self.baseURL_lazy
        finalURL_lazy = str_replace(VOTE_URL,url,finalURL_lazy)
        finalURL_lazy = str_replace(VOTE_BUTTON_DESIGN,self.getButtonDesignLazy(button),finalURL_lazy)
        finalURL_lazy = str_replace(POST_ID,postId,finalURL_lazy)
        self.finalURL_lazy = finalURL_lazy
        
        finalURL_lazy_script = self.baseURL_lazy_script
        finalURL_lazy_script = str_replace(POST_ID,postId,finalURL_lazy_script)
        self.finalURL_lazy_script = finalURL_lazy_script
        
        final_scheduler_lazy_script = self.scheduler_lazy_script
        final_scheduler_lazy_script = str_replace(SCHEDULER_TIMER,self.scheduler_lazy_timer,final_scheduler_lazy_script)
        final_scheduler_lazy_script = str_replace(POST_ID,postId,final_scheduler_lazy_script)
        self.final_scheduler_lazy_script =  final_scheduler_lazy_script
        























# NON-DEFAULTS

/******************************************************************************************
 * 
 * Pinterest
 * http:#pinterest.com/about/goodies/#button_for_websites
 *
 */
class DD_Pinterest (BaseDD):
    NAME = "Pinterest"
    URL_WEBSITE = "http:#pinterest.com"
    URL_API = "http:#pinterest.com/about/goodies/#button_for_websites"
    DEFAULT_BUTTON_WEIGHT = "10"

    BASEURL = '<a href="http:#pinterest.com/pin/create/button/?url=VOTE_URL&description=VOTE_TITLE&media=VOTE_IMAGE" class="pin-it-button" count-layout="VOTE_BUTTON_DESIGN"></a><script type="text/javascript" src="http:#assets.pinterest.com/js/pinit.js"></script>'
    BASEURL_LAZY = '<a href="http:#pinterest.com/pin/create/button/?url=VOTE_URL&description=VOTE_TITLE&media=VOTE_IMAGE" class="pin-it-button dd-pinterest-ajax-load dd-pinterest-POST_ID" count-layout="VOTE_BUTTON_DESIGN"></a>'
    BASEURL_LAZY_SCRIPT = "function loadPinterest_POST_ID(): jQuery(document).ready(function(\) { \.getScript('http:#assets.pinterest.com/js/pinit.js') }) }"
    SCHEDULER_LAZY_SCRIPT = "window.setTimeout('loadPinterest_POST_ID()',SCHEDULER_TIMER)"
    SCHEDULER_LAZY_TIMER = "1000"
    
    OPTION_APPEND_TYPE = "dd_pinterest_appendType"
    OPTION_BUTTON_DESIGN = "dd_pinterest_buttonDesign"
    OPTION_BUTTON_WEIGHT = "dd_pinterest_button_weight"
    OPTION_AJAX_LEFT_FLOAT = "dd_pinterest_ajax_left_float"
    OPTION_LAZY_LOAD = "dd_pinterest_lazy_load"
    
    buttonLayout = {
        "Normal" : "vertical",
        "Compact" : "horizontal",
        "No Count" : "none"
    )
    
    buttonLayoutLazy = {
        "Normal" : "vertical",
        "Compact" : "horizontal",
        "No Count" : "none" 
    )
    
    def DD_Pinterest() {

        self.option_append_type = self.OPTION_APPEND_TYPE
        self.option_button_design = self.OPTION_BUTTON_DESIGN
        self.option_button_weight = self.OPTION_BUTTON_WEIGHT
        self.option_ajax_left_float = self.OPTION_AJAX_LEFT_FLOAT
        self.option_lazy_load = self.OPTION_LAZY_LOAD
        
        self.baseURL_lazy = self.BASEURL_LAZY
        self.baseURL_lazy_script = self.BASEURL_LAZY_SCRIPT
        self.scheduler_lazy_script = self.SCHEDULER_LAZY_SCRIPT
        self.scheduler_lazy_timer = self.SCHEDULER_LAZY_TIMER
        
        self.button_weight_value = self.DEFAULT_BUTTON_WEIGHT
        
        self.BaseDD(self.NAME, self.URL_WEBSITE, self.URL_API, self.BASEURL)
      
    }

    #construct base URL, based on lazy value
     def constructURL(url, title, button, postId, lazy, globalcfg = ''):
         #quote - replace space with %20
        #urlencode - replace space with + 
         if(self.isEncodeRequired) {
             title = quote(title)
            url = quote(url)
         }
         
        if(lazy==DD_EMPTY_VALUE || lazy==False):
            self.constructNormalURL(url, title,button, postId)
        }else{
            self.constructLazyLoadURL(url, title,button, postId)
        }
        
    }
    
    def constructNormalURL(url, title,button, postId):
        
        finalURL = self.baseURL
        finalURL = str_replace(VOTE_BUTTON_DESIGN,self.getButtonDesign(button),finalURL)
        finalURL = str_replace(VOTE_TITLE,title,finalURL)
        finalURL = str_replace(VOTE_URL,url,finalURL)
        finalURL = str_replace(POST_ID,postId,finalURL)
        finalURL = str_replace(VOTE_TITLE,title,finalURL)
        finalURL = str_replace(VOTE_URL,url,finalURL)
        
        # If theme uses post thumbnails, grab the chosen thumbnail if not grab the first image attached to post
        if(current_theme_supports('post-thumbnails')):
            thumb = wp_get_attachment_image_src(get_post_thumbnail_id(postId), 'full')
        } else {
            image_args = {
                'order'          : 'ASC',
                'orderby'        : 'menu_order',
                'post_type'      : 'attachment',
                'post_parent'    : postId,
                'post_mime_type' : 'image',
                'post_status'    : null,
                'numberposts'    : -1,
            )
            attachments = get_posts(image_args)
              
              if (attachments) {
                  thumb = wp_get_attachment_image_src(attachments[0]->ID, 'full')
              }    
        }
        
        if(thumb):
            image = thumb[0]
        } else {
            image = ''
        }
        
        finalURL = str_replace(VOTE_IMAGE,image,finalURL)
        self.finalURL = finalURL
    }
    
    def constructLazyLoadURL(url, title,button, postId):
        
        finalURL_lazy = self.baseURL_lazy
        finalURL_lazy = str_replace(VOTE_BUTTON_DESIGN,self.getButtonDesignLazy(button),finalURL_lazy)
        finalURL_lazy = str_replace(POST_ID,postId,finalURL_lazy)
        finalURL_lazy = str_replace(VOTE_TITLE,title,finalURL_lazy)
        finalURL_lazy = str_replace(VOTE_URL,url,finalURL_lazy)
        if(current_theme_supports('post-thumbnails')) thumb = wp_get_attachment_image_src( get_post_thumbnail_id(postId), 'full' )
        else thumb = False
        if(thumb) image = thumb[0]
        else image = ''
        finalURL_lazy = str_replace(VOTE_IMAGE,image,finalURL_lazy)
        self.finalURL_lazy = finalURL_lazy
        
        finalURL_lazy_script = self.baseURL_lazy_script
        finalURL_lazy_script = str_replace(VOTE_TITLE,title,finalURL_lazy_script)
        finalURL_lazy_script = str_replace(VOTE_URL,url,finalURL_lazy_script)
        finalURL_lazy_script = str_replace(POST_ID,postId,finalURL_lazy_script)

        self.finalURL_lazy_script = finalURL_lazy_script
        
        final_scheduler_lazy_script = self.scheduler_lazy_script
        final_scheduler_lazy_script = str_replace(SCHEDULER_TIMER,self.scheduler_lazy_timer,final_scheduler_lazy_script)
        final_scheduler_lazy_script = str_replace(POST_ID,postId,final_scheduler_lazy_script)
        self.final_scheduler_lazy_script =  final_scheduler_lazy_script
        

/******************************************************************************************
 * 
 * Flattr
 * http:#developers.flattr.net/button/
 *
 */
class DD_Flattr (BaseDD):
    NAME = "Flattr"
    URL_WEBSITE = "http:#flattr.com"
    URL_API = "http:#developers.flattr.net/button/"
    DEFAULT_BUTTON_WEIGHT = "10"

    BASEURL = '<script src="http:#api.flattr.com/js/0.6/load.js?mode=auto"></script><a class="FlattrButton" href="VOTE_URL" style="display:none" title="VOTE_TITLE" data-flattr-uid="VOTE_FLATTR_UID" data-flattr-button="VOTE_BUTTON_DESIGN" data-flattr-category="text"></a>'
    BASEURL_LAZY = '<a class="FlattrButton" href="VOTE_URL" style="display:none" title="VOTE_TITLE" data-flattr-uid="VOTE_FLATTR_UID" data-flattr-button="VOTE_BUTTON_DESIGN" data-flattr-category="text"></a>'
    BASEURL_LAZY_SCRIPT = "function loadFlattr_POST_ID(): jQuery(document).ready(function(\) { \.getScript('http:#api.flattr.com/js/0.6/load.js?mode=auto') }) }"
    SCHEDULER_LAZY_SCRIPT = "window.setTimeout('loadFlattr_POST_ID()',SCHEDULER_TIMER)"
    SCHEDULER_LAZY_TIMER = "1000"

    OPTION_APPEND_TYPE = "dd_flattr_appendType"
    OPTION_BUTTON_DESIGN = "dd_flattr_buttonDesign"
    OPTION_BUTTON_WEIGHT = "dd_flattr_button_weight"
    OPTION_AJAX_LEFT_FLOAT = "dd_flattr_ajax_left_float"
    OPTION_LAZY_LOAD = "dd_flattr_lazy_load"
    
    buttonLayout = {
        "Normal" : "default",
        "Compact" : "compact"
    )
    
    buttonLayoutLazy = {
        "Normal" : "default",
        "Compact" : "compact"
    )
    
    VOTE_FLATTR_UID = 'VOTE_FLATTR_UID'
    
    def DD_Flattr() {
        
        self.option_append_type = self.OPTION_APPEND_TYPE
        self.option_button_design = self.OPTION_BUTTON_DESIGN
        self.option_button_weight = self.OPTION_BUTTON_WEIGHT
        self.option_ajax_left_float = self.OPTION_AJAX_LEFT_FLOAT
        self.option_lazy_load = self.OPTION_LAZY_LOAD
        
        self.baseURL = self.BASEURL
        self.baseURL_lazy = self.BASEURL_LAZY
        self.baseURL_lazy_script = self.BASEURL_LAZY_SCRIPT
        self.scheduler_lazy_script = self.SCHEDULER_LAZY_SCRIPT
        self.scheduler_lazy_timer = self.SCHEDULER_LAZY_TIMER
        
        self.button_weight_value = self.DEFAULT_BUTTON_WEIGHT
        
        self.BaseDD(self.NAME, self.URL_WEBSITE, self.URL_API, self.BASEURL)
      
    }

    #construct base URL, based on lazy value
     def constructURL(url, title, button, postId, lazy, globalcfg = ''):
    
        flattr_uid = 'flattr'
         if(globalcfg!=''):
             flattr_uid = globalcfg[DD_GLOBAL_FLATTR_OPTION][DD_GLOBAL_FLATTR_OPTION_UID]
            if(empty(flattr_uid)) flattr_uid = 'flattr'
         }

        if(lazy==DD_EMPTY_VALUE || lazy==False):
            self.baseURL = str_replace(VOTE_FLATTR_UID, flattr_uid, self.baseURL)
            self.constructNormalURL(url, title, button, postId)

        }else{
            self.baseURL_lazy = str_replace(VOTE_FLATTR_UID, flattr_uid, self.baseURL_lazy)
            self.constructLazyLoadURL(url, title, button, postId)
        }
        
    }
    
    def constructNormalURL(url, title, button, postId):
        
        finalURL = self.baseURL
        finalURL = str_replace(VOTE_BUTTON_DESIGN,self.getButtonDesign(button),finalURL)
        finalURL = str_replace(VOTE_TITLE,title,finalURL)
        finalURL = str_replace(VOTE_URL,url,finalURL)
        finalURL = str_replace(POST_ID,postId,finalURL)
        self.finalURL = finalURL
    }

    def constructLazyLoadURL(url, title, button, postId):
        
        finalURL_lazy = self.baseURL_lazy
        finalURL_lazy = str_replace(VOTE_BUTTON_DESIGN,self.getButtonDesignLazy(button),finalURL_lazy)
        finalURL_lazy = str_replace(VOTE_TITLE,title,finalURL_lazy)
        finalURL_lazy = str_replace(VOTE_URL,url,finalURL_lazy)
        finalURL_lazy = str_replace(POST_ID,postId,finalURL_lazy)
        self.finalURL_lazy = finalURL_lazy
        
        finalURL_lazy_script = self.baseURL_lazy_script
        finalURL_lazy_script = str_replace(POST_ID,postId,finalURL_lazy_script)
        self.finalURL_lazy_script = finalURL_lazy_script
        
        final_scheduler_lazy_script = self.scheduler_lazy_script
        final_scheduler_lazy_script = str_replace(SCHEDULER_TIMER,self.scheduler_lazy_timer,final_scheduler_lazy_script)
        final_scheduler_lazy_script = str_replace(POST_ID,postId,final_scheduler_lazy_script)
        self.final_scheduler_lazy_script =  final_scheduler_lazy_script
        


/******************************************************************************************
 * 
 * Facebook Like (IFrame)
 * 
 */
class DD_FbLike (BaseIFrameDD):
    NAME = "Facebook Like (IFrame)"
    URL_WEBSITE = "http:#www.facebook.com"
    URL_API = "http:#developers.facebook.com/docs/reference/plugins/like"
    BASEURL = "<iframe src='http:#www.facebook.com/plugins/like.php?href=VOTE_URL&amplocale=FACEBOOK_LOCALE&ampVOTE_BUTTON_DESIGN' scrolling='no' frameborder='0' style='border:none overflow:hidden EXTRA_VALUE' allowTransparency='True'></iframe>"
    
    FB_LOCALES = "http:#www.facebook.com/translations/FacebookLocales.xml"
    DEFAULT_BUTTON_WEIGHT = "96"
    
    OPTION_APPEND_TYPE = "dd_fblike_appendType"
    OPTION_BUTTON_DESIGN = "dd_fblike_buttonDesign"
    OPTION_BUTTON_WEIGHT = "dd_fblike_button_weight"
    OPTION_AJAX_LEFT_FLOAT = "dd_fblike_ajax_left_float"
    OPTION_LAZY_LOAD = "dd_fblike_lazy_load"
    
    BASEURL_LAZY = "<div class='dd-fblike-ajax-load dd-fblike-POST_ID'></div><iframe class="DD_FBLIKE_AJAX_POST_ID" src='' height='0' width='0' scrolling='no' frameborder='0' allowTransparency='True'></iframe>"
    BASEURL_LAZY_SCRIPT = " function loadFBLike_POST_ID(): jQuery(document).ready(function(\) { \('.dd-fblike-POST_ID').remove()\('.DD_FBLIKE_AJAX_POST_ID').attr('width','VOTE_BUTTON_DESIGN_LAZY_WIDTH')\('.DD_FBLIKE_AJAX_POST_ID').attr('height','VOTE_BUTTON_DESIGN_LAZY_HEIGHT')\('.DD_FBLIKE_AJAX_POST_ID').attr('src','http:#www.facebook.com/plugins/like.php?href=VOTE_URL&amplocale=FACEBOOK_LOCALE&ampVOTE_BUTTON_DESIGN') }) }"
    SCHEDULER_LAZY_SCRIPT = "window.setTimeout('loadFBLike_POST_ID()',SCHEDULER_TIMER)"
    SCHEDULER_LAZY_TIMER = "1000"
    
    LIKE_STANDARD = "layout=standard&ampaction=like&ampwidth=350&ampheight=24&ampcolorscheme=light" #350x24
    LIKE_BUTTON_COUNT= "layout=button_count&ampaction=like&ampwidth=92&ampheight=20&ampcolorscheme=light" #92x20
    LIKE_BOX_COUNT= "layout=box_count&ampaction=like&ampwidth=50&ampheight=60&ampcolorscheme=light" #50x60
    RECOMMEND_STANDARD = "layout=standard&ampaction=recommend&ampwidth=400&ampheight=24&ampcolorscheme=light" #400x24
    RECOMMEND_BUTTON_COUNT= "layout=button_count&ampaction=recommend&ampwidth=130&ampheight=20&ampcolorscheme=light" #130x20
    RECOMMEND_BOX_COUNT= "layout=box_count&ampaction=recommend&ampwidth=90&ampheight=60&ampcolorscheme=light" #90x60

    EXTRA_VALUE = "EXTRA_VALUE"
    FACEBOOK_LOCALE = "FACEBOOK_LOCALE"
    
    float_button_design = "Like Box Count"
    
    buttonLayout = {
        "Like Standard" : self.LIKE_STANDARD,
        "Like Button Count" : self.LIKE_BUTTON_COUNT,
        "Like Box Count" : self.LIKE_BOX_COUNT,
        "Recommend Standard" : self.RECOMMEND_STANDARD,
        "Recommend Button Count" : self.RECOMMEND_BUTTON_COUNT,
        "Recommend Box Count" : self.RECOMMEND_BOX_COUNT
    )
    
    buttonLayoutLazy = {
        "Like Standard" : self.LIKE_STANDARD,
        "Like Button Count" : self.LIKE_BUTTON_COUNT,
        "Like Box Count" : self.LIKE_BOX_COUNT,
        "Recommend Standard" : self.RECOMMEND_STANDARD,
        "Recommend Button Count" : self.RECOMMEND_BUTTON_COUNT,
        "Recommend Box Count" : self.RECOMMEND_BOX_COUNT
    )
    
    buttonLayoutWidthHeight = {
        "Like Standard" : "width:500px height:24px",
        "Like Button Count" : "width:92px height:20px",
        "Like Box Count" : "width:50px height:62px",
        "Recommend Standard" : "width:500px height:24px",
        "Recommend Button Count" : "width:130px height:20px",
        "Recommend Box Count" : "width:90px height:60px"
    )
    
    buttonLayoutLazyWidth = {
        "Like Standard" : "500",
        "Like Button Count" : "92",
        "Like Box Count" : "50",
        "Recommend Standard" : "500",
        "Recommend Button Count" : "130",
        "Recommend Box Count" : "90"
    )
    
    buttonLayoutLazyHeight = {
        "Like Standard" : "24",
        "Like Button Count" : "20",
        "Like Box Count" : "62",
        "Recommend Standard" : "24",
        "Recommend Button Count" : "20",
        "Recommend Box Count" : "60"
    )
    
    def DD_FbLike() {
        
        self.option_append_type = self.OPTION_APPEND_TYPE
        self.option_button_design = self.OPTION_BUTTON_DESIGN
        self.option_button_weight = self.OPTION_BUTTON_WEIGHT
        self.option_ajax_left_float = self.OPTION_AJAX_LEFT_FLOAT
        self.option_lazy_load = self.OPTION_LAZY_LOAD
        
        self.baseURL_lazy = self.BASEURL_LAZY
        self.baseURL_lazy_script = self.BASEURL_LAZY_SCRIPT
        self.scheduler_lazy_script = self.SCHEDULER_LAZY_SCRIPT
        self.scheduler_lazy_timer = self.SCHEDULER_LAZY_TIMER
        
        self.button_weight_value = self.DEFAULT_BUTTON_WEIGHT
        
         self.BaseDD(self.NAME, self.URL_WEBSITE, self.URL_API, self.BASEURL)
        
    } 
    
    def constructLazyLoadURL(url, title,button, postId):
        
        finalURL_lazy = self.baseURL_lazy
        finalURL_lazy = str_replace(VOTE_BUTTON_DESIGN,self.getButtonDesignLazy(button),finalURL_lazy)
        finalURL_lazy = str_replace(VOTE_TITLE,title,finalURL_lazy)
        finalURL_lazy = str_replace(VOTE_URL,url,finalURL_lazy)
        finalURL_lazy = str_replace(POST_ID,postId,finalURL_lazy)    
        self.finalURL_lazy = finalURL_lazy
        
        finalURL_lazy_script = self.baseURL_lazy_script
        finalURL_lazy_script = str_replace(VOTE_BUTTON_DESIGN_LAZY_WIDTH,self.getButtonDesignLazyWidth(button),finalURL_lazy_script)
        finalURL_lazy_script = str_replace(VOTE_BUTTON_DESIGN_LAZY_HEIGHT,self.getButtonDesignLazyHeight(button),finalURL_lazy_script)
        finalURL_lazy_script = str_replace(VOTE_BUTTON_DESIGN,self.getButtonDesignLazy(button),finalURL_lazy_script)
        finalURL_lazy_script = str_replace(VOTE_TITLE,title,finalURL_lazy_script)
        finalURL_lazy_script = str_replace(VOTE_URL,url,finalURL_lazy_script)
        finalURL_lazy_script = str_replace(POST_ID,postId,finalURL_lazy_script)
        
        #add new line
        #convert &amp to &
        finalURL_lazy_script = str_replace("&amp","&",finalURL_lazy_script)
        self.finalURL_lazy_script = finalURL_lazy_script
        
        final_scheduler_lazy_script = self.scheduler_lazy_script
        final_scheduler_lazy_script = str_replace(SCHEDULER_TIMER,self.scheduler_lazy_timer,final_scheduler_lazy_script)
        final_scheduler_lazy_script = str_replace(POST_ID,postId,final_scheduler_lazy_script)
        self.final_scheduler_lazy_script =  final_scheduler_lazy_script
        
    }
    
    def constructURL(url, title,button, postId, lazy, globalcfg = ''):
        
         if(self.isEncodeRequired):
             title = quote(title)
            url = quote(url)
         }
         
         facebook_locale = ''
         if(globalcfg!=''):
             facebook_locale = globalcfg[DD_GLOBAL_FACEBOOK_OPTION][DD_GLOBAL_FACEBOOK_OPTION_LOCALE] 
         }
    
        if(lazy==DD_EMPTY_VALUE):

            self.baseURL = str_replace(self.FACEBOOK_LOCALE,facebook_locale,self.baseURL)
            self.constructNormalURL(url, title,button, postId)
            
        }else{

            self.baseURL_lazy_script = str_replace(self.FACEBOOK_LOCALE,facebook_locale,self.baseURL_lazy_script)
            self.constructLazyLoadURL(url, title,button, postId)
            
        }
        


/******************************************************************************************
 *  
 * http:#www.digg.com
 *
 */
class DD_Digg (BaseDD):
    
    NAME = "Digg"
    URL_WEBSITE = "http:#www.digg.com"
    URL_API = "http:#about.digg.com/downloads/button/smart"
    DEFAULT_BUTTON_WEIGHT = "95"
    
    BASEURL = "<script type='text/javascript'>(function() {s = document.createElement('SCRIPT'), s1 = document.getElementsByTagName('SCRIPT')[0]s.type = 'text/javascript's.async = Trues.src = 'http:#widgets.digg.com/buttons.js's1.parentNode.insertBefore(s, s1)})()</script> <a class='DiggThisButton VOTE_BUTTON_DESIGN' href='http:#digg.com/submit?url=VOTE_URL&amptitle=VOTE_TITLE'></a>"
    BASEURL_LAZY = "<div class='dd-digg-ajax-load dd-digg-POST_ID'></div><a class='DiggThisButton DD_DIGG_AJAX_POST_ID VOTE_BUTTON_DESIGN'></a>"
    BASEURL_LAZY_SCRIPT = " function loadDigg_POST_ID(): jQuery(document).ready(function(\) { \('.dd-digg-POST_ID').remove()\('.DD_DIGG_AJAX_POST_ID').attr('href','http:#digg.com/submit?url=VOTE_URL&amptitle=VOTE_TITLE')\.getScript('http:#widgets.digg.com/buttons.js') }) }"
    SCHEDULER_LAZY_SCRIPT = "window.setTimeout('loadDigg_POST_ID()',SCHEDULER_TIMER)"
    SCHEDULER_LAZY_TIMER = "1000"
    
    OPTION_APPEND_TYPE = "dd_digg_appendType"
    OPTION_BUTTON_DESIGN = "dd_digg_buttonDesign"
    OPTION_BUTTON_WEIGHT = "dd_digg_button_weight"
    OPTION_AJAX_LEFT_FLOAT = "dd_digg_ajax_left_float"
    OPTION_LAZY_LOAD = "dd_digg_lazy_load"
    
    buttonLayout = {
        "Wide" : "DiggWide",
        "Normal" : "DiggMedium",
        "Compact" : "DiggCompact",
        "Icon" : "DiggIcon" 
    )
    
    buttonLayoutLazy = {
        "Wide" : "DiggWide",
        "Normal" : "DiggMedium",
        "Compact" : "DiggCompact",
        "Icon" : "DiggIcon" 
    )
    
    def DD_Digg() {
        
        self.option_append_type = self.OPTION_APPEND_TYPE
        self.option_button_design = self.OPTION_BUTTON_DESIGN
        self.option_button_weight = self.OPTION_BUTTON_WEIGHT
        self.option_ajax_left_float = self.OPTION_AJAX_LEFT_FLOAT
        self.option_lazy_load = self.OPTION_LAZY_LOAD
        
        self.baseURL_lazy = self.BASEURL_LAZY
        self.baseURL_lazy_script = self.BASEURL_LAZY_SCRIPT
        self.scheduler_lazy_script = self.SCHEDULER_LAZY_SCRIPT
        self.scheduler_lazy_timer = self.SCHEDULER_LAZY_TIMER
        
        self.button_weight_value = self.DEFAULT_BUTTON_WEIGHT
        
        self.BaseDD(self.NAME, self.URL_WEBSITE, self.URL_API, self.BASEURL)
      
    }
    
    def constructLazyLoadURL(url, title,button, postId):
        
        finalURL_lazy = self.baseURL_lazy
        finalURL_lazy = str_replace(VOTE_BUTTON_DESIGN,self.getButtonDesignLazy(button),finalURL_lazy)
        finalURL_lazy = str_replace(POST_ID,postId,finalURL_lazy)
        self.finalURL_lazy = finalURL_lazy
        
        finalURL_lazy_script = self.baseURL_lazy_script
        finalURL_lazy_script = str_replace(VOTE_TITLE,title,finalURL_lazy_script)
        finalURL_lazy_script = str_replace(VOTE_URL,url,finalURL_lazy_script)
        finalURL_lazy_script = str_replace(POST_ID,postId,finalURL_lazy_script)
        self.finalURL_lazy_script = finalURL_lazy_script
        
        final_scheduler_lazy_script = self.scheduler_lazy_script
        final_scheduler_lazy_script = str_replace(SCHEDULER_TIMER,self.scheduler_lazy_timer,final_scheduler_lazy_script)
        final_scheduler_lazy_script = str_replace(POST_ID,postId,final_scheduler_lazy_script)
        self.final_scheduler_lazy_script =  final_scheduler_lazy_script
        


/******************************************************************************************
 * 
 * http:#www.reddit.com
 *
 */
class DD_Reddit (BaseIFrameDD):
    
    NAME = "Reddit"
    URL_WEBSITE = "http:#www.reddit.com"
    URL_API = "http:#www.reddit.com/buttons/"
    DEFAULT_BUTTON_WEIGHT = "99"
    
    BASEURL = "<iframe src="http:#www.reddit.com/static/button/VOTE_BUTTON_DESIGN&url=VOTE_URL&title=VOTE_TITLE&newwindow='1'" EXTRA_VALUE scrolling='no' frameborder='0'></iframe>"
    
    BASEURL_LAZY = "<div class='dd-reddit-ajax-load dd-reddit-POST_ID'></div><iframe class='DD_REDDIT_AJAX_POST_ID' src='' height='0' width='0' scrolling='no' frameborder='0'></iframe>"
    BASEURL_LAZY_SCRIPT = " function loadReddit_POST_ID(): jQuery(document).ready(function(\) { \('.dd-reddit-POST_ID').remove()\('.DD_REDDIT_AJAX_POST_ID').attr('width','VOTE_BUTTON_DESIGN_LAZY_WIDTH')\('.DD_REDDIT_AJAX_POST_ID').attr('height','VOTE_BUTTON_DESIGN_LAZY_HEIGHT')\('.DD_REDDIT_AJAX_POST_ID').attr('src','http:#www.reddit.com/static/button/VOTE_BUTTON_DESIGN&url=VOTE_URL&title=VOTE_TITLE&newwindow=1') }) }"
    SCHEDULER_LAZY_SCRIPT = "window.setTimeout('loadReddit_POST_ID()',SCHEDULER_TIMER)"
    SCHEDULER_LAZY_TIMER = "1000"
    
    OPTION_APPEND_TYPE = "dd_reddit_appendType"
    OPTION_BUTTON_DESIGN = "dd_reddit_buttonDesign"
    OPTION_BUTTON_WEIGHT = "dd_reddit_button_weight"
    OPTION_AJAX_LEFT_FLOAT = "dd_reddit_ajax_left_float"
    OPTION_LAZY_LOAD = "dd_reddit_lazy_load"
    
    buttonLayout = {
        "Normal" : "button2.html?width=51", 
        "Compact" : "button1.html?width=120", 
        "Icon" : "button3.html?width=69"
    )
    
    buttonLayoutLazy = {
        "Normal" : "button2.html?width=51", 
        "Compact" : "button1.html?width=120", 
        "Icon" : "button3.html?width=69"
    )
    
    buttonLayoutLazyWidth = {
        "Normal" : "51",
        "Compact" : "120",
        "Icon" : "69"
    )
    
    buttonLayoutLazyHeight = {
        "Normal" : "69",
        "Compact" : "22",
        "Icon" : "52"
    )
    
    buttonLayoutWidthHeight = {
        "Normal" : "height="69" width="51"",
        "Compact" : "height="22" width="120"",
        "Icon" : "height="52" width="69""
    )
    
    def DD_Reddit() {
        
        self.option_append_type = self.OPTION_APPEND_TYPE
        self.option_button_design = self.OPTION_BUTTON_DESIGN
        self.option_button_weight = self.OPTION_BUTTON_WEIGHT
        self.option_ajax_left_float = self.OPTION_AJAX_LEFT_FLOAT
        self.option_lazy_load = self.OPTION_LAZY_LOAD
            
        self.baseURL_lazy = self.BASEURL_LAZY
        self.baseURL_lazy_script = self.BASEURL_LAZY_SCRIPT
        self.scheduler_lazy_script = self.SCHEDULER_LAZY_SCRIPT
        self.scheduler_lazy_timer = self.SCHEDULER_LAZY_TIMER
        
        self.button_weight_value = self.DEFAULT_BUTTON_WEIGHT
        
         self.BaseDD(self.NAME, self.URL_WEBSITE, self.URL_API, self.BASEURL)

/******************************************************************************************
 * 
 * http:#www.google.com/buzz
 *
 */
class DD_GBuzz (BaseDD):
    
    NAME = "Google Buzz"
    URL_WEBSITE = "http:#www.google.com/buzz"
    URL_API = "http:#www.google.com/buzz/api/admin/configPostWidget"
    URL_API2 = "http:#code.google.com/apis/buzz/buttons_and_gadgets.html"
    DEFAULT_BUTTON_WEIGHT = "98"
    
    BASEURL = "<a title='Post on Google Buzz' class='google-buzz-button' href='http:#www.google.com/buzz/post' data-button-style='VOTE_BUTTON_DESIGN' data-url='VOTE_URL'></a><script type='text/javascript' src='http:#www.google.com/buzz/api/button.js'></script>"

    OPTION_APPEND_TYPE = "dd_gbuzz_appendType"
    OPTION_BUTTON_DESIGN = "dd_gbuzz_buttonDesign"
    OPTION_BUTTON_WEIGHT = "dd_gbuzz_button_weight"
    OPTION_AJAX_LEFT_FLOAT = "dd_gbuzz_ajax_left_float"
    OPTION_LAZY_LOAD = "dd_gbuzz_lazy_load"
    
    BASEURL_LAZY = "<div class='dd-gbuzz-ajax-load dd-gbuzz-POST_ID'></div><a title='Post on Google Buzz' class='google-buzz-button' href='http:#www.google.com/buzz/post' data-button-style='VOTE_BUTTON_DESIGN' data-url='VOTE_URL'></a>"
    BASEURL_LAZY_SCRIPT = " function loadGBuzz_POST_ID(): jQuery(document).ready(function(\) { \('.dd-gbuzz-POST_ID').remove()\.getScript('http:#www.google.com/buzz/api/button.js') }) }"
    SCHEDULER_LAZY_SCRIPT = "window.setTimeout('loadGBuzz_POST_ID()',SCHEDULER_TIMER)"
    SCHEDULER_LAZY_TIMER = "1000"
    
    buttonLayout = {
        "Normal" : "normal-count", 
        "Compact" : "small-count"
    )
    
    buttonLayoutLazy = {
        "Normal" : "normal-count", 
        "Compact" : "small-count"
    )

    isEncodeRequired = False
    
    def DD_GBuzz() {
        
        self.option_append_type = self.OPTION_APPEND_TYPE
        self.option_button_design = self.OPTION_BUTTON_DESIGN
        self.option_button_weight = self.OPTION_BUTTON_WEIGHT
        self.option_ajax_left_float = self.OPTION_AJAX_LEFT_FLOAT
        self.option_lazy_load = self.OPTION_LAZY_LOAD
        
        self.baseURL_lazy = self.BASEURL_LAZY
        self.baseURL_lazy_script = self.BASEURL_LAZY_SCRIPT
        self.scheduler_lazy_script = self.SCHEDULER_LAZY_SCRIPT
        self.scheduler_lazy_timer = self.SCHEDULER_LAZY_TIMER
        
        self.button_weight_value = self.DEFAULT_BUTTON_WEIGHT
        
         self.BaseDD(self.NAME, self.URL_WEBSITE, self.URL_API, self.BASEURL)
        
    }
  
    def constructLazyLoadURL(url, title,button, postId):
        
        finalURL_lazy = self.baseURL_lazy
        finalURL_lazy = str_replace(VOTE_URL,url,finalURL_lazy)
        finalURL_lazy = str_replace(VOTE_BUTTON_DESIGN,self.getButtonDesignLazy(button),finalURL_lazy)
        finalURL_lazy = str_replace(POST_ID,postId,finalURL_lazy)
        self.finalURL_lazy = finalURL_lazy
        
        finalURL_lazy_script = self.baseURL_lazy_script
        finalURL_lazy_script = str_replace(POST_ID,postId,finalURL_lazy_script)
        self.finalURL_lazy_script = finalURL_lazy_script
        
        final_scheduler_lazy_script = self.scheduler_lazy_script
        final_scheduler_lazy_script = str_replace(SCHEDULER_TIMER,self.scheduler_lazy_timer,final_scheduler_lazy_script)
        final_scheduler_lazy_script = str_replace(POST_ID,postId,final_scheduler_lazy_script)
        self.final_scheduler_lazy_script =  final_scheduler_lazy_script
        

/******************************************************************************************
 * 
 * http:#www.dzone.com
 *
 */
class DD_DZone (BaseDD):
    
    NAME = "DZone"
    URL_WEBSITE = "http:#www.dzone.com"
    URL_API = "http:#www.dzone.com/links/buttons.jsp"
    BASEURL = "<iframe src='http:#widgets.dzone.com/links/widgets/zoneit.html?url=VOTE_URL&amptitle=VOTE_TITLE&ampt=VOTE_BUTTON_DESIGN frameborder='0' scrolling='no'></iframe>"
    
    BASEURL_LAZY = "<div class='dd-dzone-ajax-load dd-dzone-POST_ID'></div><iframe class='DD_DZONE_AJAX_POST_ID' src='' height='0' width='0' scrolling='no' frameborder='0'></iframe>"
    BASEURL_LAZY_SCRIPT = " function loadDzone_POST_ID(): jQuery(document).ready(function(\) { \('.dd-dzone-POST_ID').remove()\('.DD_DZONE_AJAX_POST_ID').attr('width','VOTE_BUTTON_DESIGN_LAZY_WIDTH')\('.DD_DZONE_AJAX_POST_ID').attr('height','VOTE_BUTTON_DESIGN_LAZY_HEIGHT')\('.DD_DZONE_AJAX_POST_ID').attr('src','http:#widgets.dzone.com/links/widgets/zoneit.html?url=VOTE_URL&title=VOTE_TITLE&t=VOTE_BUTTON_DESIGN') }) }"
    SCHEDULER_LAZY_SCRIPT = "window.setTimeout('loadDzone_POST_ID()',SCHEDULER_TIMER)"
    SCHEDULER_LAZY_TIMER = "1000"
    
    OPTION_APPEND_TYPE = "dd_dzone_appendType"
    OPTION_BUTTON_DESIGN = "dd_dzone_buttonDesign"
    OPTION_BUTTON_WEIGHT = "dd_dzone_button_weight"
    OPTION_AJAX_LEFT_FLOAT = "dd_dzone_ajax_left_float"
    OPTION_LAZY_LOAD = "dd_dzone_lazy_load"
    
    DEFAULT_BUTTON_WEIGHT = "97"

    buttonLayout = {
        "Normal" : "1' height='70' width='50'", 
        "Compact" : "2' height='25' width='155'"
    )
    
    buttonLayoutLazy = {
        "Normal" : "1", 
        "Compact" : "2"
    )
    
    buttonLayoutLazyWidth = {
        "Normal" : "50",
        "Compact" : "155"
    )
    
    buttonLayoutLazyHeight = {
        "Normal" : "70",
        "Compact" : "25"
    )
    
    def DD_DZone() {
        
        self.option_append_type = self.OPTION_APPEND_TYPE
        self.option_button_design = self.OPTION_BUTTON_DESIGN
        self.option_button_weight = self.OPTION_BUTTON_WEIGHT
        self.option_ajax_left_float = self.OPTION_AJAX_LEFT_FLOAT
        self.option_lazy_load = self.OPTION_LAZY_LOAD
        
        self.baseURL_lazy = self.BASEURL_LAZY
        self.baseURL_lazy_script = self.BASEURL_LAZY_SCRIPT
        self.scheduler_lazy_script = self.SCHEDULER_LAZY_SCRIPT
        self.scheduler_lazy_timer = self.SCHEDULER_LAZY_TIMER
        
        self.button_weight_value = self.DEFAULT_BUTTON_WEIGHT
        
        self.BaseDD(self.NAME, self.URL_WEBSITE, self.URL_API, self.BASEURL)
    } 
  
    def constructLazyLoadURL(url, title,button, postId):
        
        finalURL_lazy = self.baseURL_lazy
        finalURL_lazy = str_replace(POST_ID,postId,finalURL_lazy)
        self.finalURL_lazy = finalURL_lazy
        
        finalURL_lazy_script = self.baseURL_lazy_script
        finalURL_lazy_script = str_replace(VOTE_BUTTON_DESIGN_LAZY_WIDTH,self.getButtonDesignLazyWidth(button),finalURL_lazy_script)
        finalURL_lazy_script = str_replace(VOTE_BUTTON_DESIGN_LAZY_HEIGHT,self.getButtonDesignLazyHeight(button),finalURL_lazy_script)
        finalURL_lazy_script = str_replace(VOTE_BUTTON_DESIGN,self.getButtonDesignLazy(button),finalURL_lazy_script)
        finalURL_lazy_script = str_replace(VOTE_TITLE,title,finalURL_lazy_script)
        finalURL_lazy_script = str_replace(VOTE_URL,url,finalURL_lazy_script)
        finalURL_lazy_script = str_replace(POST_ID,postId,finalURL_lazy_script)
        self.finalURL_lazy_script = finalURL_lazy_script
        
        final_scheduler_lazy_script = self.scheduler_lazy_script
        final_scheduler_lazy_script = str_replace(SCHEDULER_TIMER,self.scheduler_lazy_timer,final_scheduler_lazy_script)
        final_scheduler_lazy_script = str_replace(POST_ID,postId,final_scheduler_lazy_script)
        self.final_scheduler_lazy_script =  final_scheduler_lazy_script
        
"""

class DD_FbShare(BaseDD):

    NAME = "Facebook Share"
    URL_WEBSITE = "http:#www.facebook.com"
    URL_API = "http:#www.facebook.com/share/"
    BASEURL = """<a name='fb_share' type='VOTE_BUTTON_DESIGN' share_url='VOTE_URL' href='http://www.facebook.com/sharer.php'></a><script src='http://static.ak.fbcdn.net/connect.php/js/FB.Share' type='text/javascript'></script>"""
    DEFAULT_BUTTON_WEIGHT = "95"

    OPTION_APPEND_TYPE = "dd_fbshare_appendType"
    OPTION_BUTTON_DESIGN = "dd_fbshare_buttonDesign"
    OPTION_BUTTON_WEIGHT = "dd_fbshare_button_weight"
    OPTION_AJAX_LEFT_FLOAT = "dd_fbshare_ajax_left_float"
    OPTION_LAZY_LOAD = "dd_fbshare_lazy_load"

    BASEURL_LAZY = "<div class='dd-fbshare-ajax-load dd-fbshare-POST_ID'></div><a class='DD_FBSHARE_AJAX_POST_ID' name='fb_share' type='VOTE_BUTTON_DESIGN' share_url='VOTE_URL' href='http://www.facebook.com/sharer.php'></a>";
    BASEURL_LAZY_SCRIPT = " function loadFBShare_POST_ID(){ jQuery(document).ready(function(\$) { \$('.dd-fbshare-POST_ID').remove(); \$.getScript('http://static.ak.fbcdn.net/connect.php/js/FB.Share'); }); }";
    SCHEDULER_LAZY_SCRIPT = "window.setTimeout('loadFBShare_POST_ID()',SCHEDULER_TIMER);";
    SCHEDULER_LAZY_TIMER = "1000"

    buttonLayout = {
        "Normal": "box_count",
        "Compact": "button_count"
    }

    buttonLayoutLazy = {
        "Normal": "box_count",
        "Compact": "button_count"
    }

    isEncodeRequired = False

    def __init__(self, context, request):

        self.option_append_type = self.OPTION_APPEND_TYPE
        self.option_button_design = self.OPTION_BUTTON_DESIGN
        self.option_button_weight = self.OPTION_BUTTON_WEIGHT
        self.option_ajax_left_float = self.OPTION_AJAX_LEFT_FLOAT
        self.option_lazy_load = self.OPTION_LAZY_LOAD

        self.baseURL_lazy = self.BASEURL_LAZY
        self.baseURL_lazy_script = self.BASEURL_LAZY_SCRIPT
        self.scheduler_lazy_script = self.SCHEDULER_LAZY_SCRIPT
        self.scheduler_lazy_timer = self.SCHEDULER_LAZY_TIMER

        self.button_weight_value = self.DEFAULT_BUTTON_WEIGHT

        BaseDD.__init__(self, self.NAME, self.URL_WEBSITE, self.URL_API,
                        self.BASEURL)

    def constructLazyLoadURL(self, url, title, button, postId):

        finalURL_lazy = self.baseURL_lazy
        finalURL_lazy = finalURL_lazy.replace(VOTE_URL, url)
        finalURL_lazy = finalURL_lazy.replace(VOTE_BUTTON_DESIGN,
                                          self.getButtonDesignLazy(button))
        finalURL_lazy = finalURL_lazy.replace(POST_ID, postId)
        self.finalURL_lazy = finalURL_lazy

        lazy_script = self.baseURL_lazy_script
        lazy_script = lazy_script.replace(POST_ID, postId)
        self.finalURL_lazy_script = lazy_script

        lazy_script = self.scheduler_lazy_script
        lazy_script = lazy_script.replace(SCHEDULER_TIMER,
                                          self.scheduler_lazy_timer)
        lazy_script = lazy_script.replace(POST_ID, postId)
        self.final_scheduler_lazy_script = lazy_script


"""
/******************************************************************************************
 * 
 * http:#www.fbshare.me
 * 
 */
class DD_FbShareMe (BaseDD):
    
    NAME = "fbShare.me"
    URL_WEBSITE = "http:#www.fbshare.me"
    URL_API = "http:#www.fbshare.me"
    DEFAULT_BUTTON_WEIGHT = "94"
    
    BASEURL = "<script>fbShare = {url: 'VOTE_URL',size: 'VOTE_BUTTON_DESIGN',}</script><script src='http:#widgets.fbshare.me/files/fbshare.js'></script>"

    OPTION_APPEND_TYPE = "dd_fbshareme_appendType"
    OPTION_BUTTON_DESIGN = "dd_fbshareme_buttonDesign"
    OPTION_BUTTON_WEIGHT = "dd_fbshareme_button_weight"
    OPTION_AJAX_LEFT_FLOAT = "dd_fbshareme_ajax_left_float"
    OPTION_LAZY_LOAD = "dd_fbshareme_lazy_load"

    BASEURL_LAZY = "<div class='dd-fbshareme-ajax-load dd-fbshareme-POST_ID'></div><iframe class="DD_FBSHAREME_AJAX_POST_ID" src='' height='0' width='0' scrolling='no' frameborder='0' allowtransparency='True'></iframe>"
    BASEURL_LAZY_SCRIPT = " function loadFBShareMe_POST_ID(): jQuery(document).ready(function(\) { \('.dd-fbshareme-POST_ID').remove()\('.DD_FBSHAREME_AJAX_POST_ID').attr('width','VOTE_BUTTON_DESIGN_LAZY_WIDTH')\('.DD_FBSHAREME_AJAX_POST_ID').attr('height','VOTE_BUTTON_DESIGN_LAZY_HEIGHT')\('.DD_FBSHAREME_AJAX_POST_ID').attr('src','http:#widgets.fbshare.me/files/fbshare.php?url=VOTE_URL&size=VOTE_BUTTON_DESIGN')  }) }"
    SCHEDULER_LAZY_SCRIPT = "window.setTimeout('loadFBShareMe_POST_ID()',SCHEDULER_TIMER)"
    SCHEDULER_LAZY_TIMER = "1000"
    
    buttonLayout = {
        "Normal" : "large",
        "Compact" : "small"
    )
    
    buttonLayoutLazy = {
        "Normal" : "large",
        "Compact" : "small"
    )
    
    buttonLayoutLazyWidth = {
        "Normal" : "53",
        "Compact" : "80"
    )
    
    buttonLayoutLazyHeight = {
        "Normal" : "69",
        "Compact" : "18"
    )
    
    isEncodeRequired = False
    
    def DD_FbShareMe() {
        
        self.option_append_type = self.OPTION_APPEND_TYPE
        self.option_button_design = self.OPTION_BUTTON_DESIGN
        self.option_button_weight = self.OPTION_BUTTON_WEIGHT
        self.option_ajax_left_float = self.OPTION_AJAX_LEFT_FLOAT
        self.option_lazy_load = self.OPTION_LAZY_LOAD
        
        self.baseURL_lazy = self.BASEURL_LAZY
        self.baseURL_lazy_script = self.BASEURL_LAZY_SCRIPT
        self.scheduler_lazy_script = self.SCHEDULER_LAZY_SCRIPT
        self.scheduler_lazy_timer = self.SCHEDULER_LAZY_TIMER

        self.button_weight_value = self.DEFAULT_BUTTON_WEIGHT
        
         self.BaseDD(self.NAME, self.URL_WEBSITE, self.URL_API, self.BASEURL)
      
    }
 
    def constructLazyLoadURL(url, title,button, postId):
        
        finalURL_lazy = self.baseURL_lazy
        finalURL_lazy = str_replace(POST_ID,postId,finalURL_lazy)
        self.finalURL_lazy = finalURL_lazy
        
        finalURL_lazy_script = self.baseURL_lazy_script
        finalURL_lazy_script = str_replace(VOTE_BUTTON_DESIGN_LAZY_WIDTH,self.getButtonDesignLazyWidth(button),finalURL_lazy_script)
        finalURL_lazy_script = str_replace(VOTE_BUTTON_DESIGN_LAZY_HEIGHT,self.getButtonDesignLazyHeight(button),finalURL_lazy_script)
        finalURL_lazy_script = str_replace(VOTE_BUTTON_DESIGN,self.getButtonDesignLazy(button),finalURL_lazy_script)
        finalURL_lazy_script = str_replace(VOTE_TITLE,title,finalURL_lazy_script)
        finalURL_lazy_script = str_replace(VOTE_URL,url,finalURL_lazy_script)
        finalURL_lazy_script = str_replace(POST_ID,postId,finalURL_lazy_script)
        self.finalURL_lazy_script = finalURL_lazy_script
        
        final_scheduler_lazy_script = self.scheduler_lazy_script
        final_scheduler_lazy_script = str_replace(SCHEDULER_TIMER,self.scheduler_lazy_timer,final_scheduler_lazy_script)
        final_scheduler_lazy_script = str_replace(POST_ID,postId,final_scheduler_lazy_script)
        self.final_scheduler_lazy_script =  final_scheduler_lazy_script
        




/******************************************************************************************
 * 
 * http:#www.delicious.com
 * 
 */
class DD_Delicious (BaseDD):
    
    NAME = "Delicious"
    URL_WEBSITE = "http:#www.delicious.com"
    URL_API = "http:#www.delicious.com/help/feeds"
    DEFAULT_BUTTON_WEIGHT = "93"
    
    BASEURL = "<div class='VOTE_BUTTON_DESIGN dd_delicious'><a class='VOTE_BUTTON_DESIGN' href='http:#delicious.com/save' onclick="window.open('http:#delicious.com/save?v=5&ampnoui&ampjump=close&ampurl='+encodeURIComponent('VOTE_URL')+'&amptitle='+encodeURIComponent('VOTE_TITLE'),'delicious', 'toolbar=no,width=550,height=550') return False"><span id='DD_DELICIOUS_AJAX_POST_ID'><div style='padding-top:3px'>SAVED_COUNT</div></span></a></div>"
    
    OPTION_APPEND_TYPE = "dd_delicious_appendType"
    OPTION_BUTTON_DESIGN = "dd_delicious_buttonDesign"
    OPTION_BUTTON_WEIGHT = "dd_delicious_button_weight"
    OPTION_AJAX_LEFT_FLOAT = "dd_delicious_ajax_left_float"
    OPTION_LAZY_LOAD = "dd_delicious_lazy_load"

    BASEURL_LAZY = "<div class='VOTE_BUTTON_DESIGN dd_delicious'><a href='http:#delicious.com/save' onclick="window.open('http:#delicious.com/save?v=5&ampnoui&ampjump=close&ampurl='+encodeURIComponent('VOTE_URL')+'&amptitle='+encodeURIComponent('VOTE_TITLE'),'delicious', 'toolbar=no,width=550,height=550') return False"><span id='DD_DELICIOUS_AJAX_POST_ID'>SAVED_COUNT</span></a></div>"
    BASEURL_LAZY_SCRIPT = " function loadDelicious_POST_ID(): jQuery(document).ready(function(\) { \('.dd-delicious-POST_ID').remove()\.getJSON('http:#feeds.delicious.com/v2/json/urlinfo/data?url=VOTE_URL&ampcallback=?',function(data) {msg =''count = 0if (data.length > 0) {count = data[0].total_postsif(count ==0):msg = '0'}else if(count ==1):msg = '1'}else{msg = count}}else{msg = '0'}\('#DD_DELICIOUS_AJAX_POST_ID').text(msg)}) }) }"
    SCHEDULER_LAZY_SCRIPT = "window.setTimeout('loadDelicious_POST_ID()',SCHEDULER_TIMER)"
    SCHEDULER_LAZY_TIMER = "1000"
    
    SAVED_COUNT = "SAVED_COUNT"

    isEncodeRequired = False
    
    buttonLayout = {
        "Normal" : DD_PLUGIN_STYLE_DELICIOUS,
        "Compact" : DD_PLUGIN_STYLE_DELICIOUS_COMPACT
    )
    
    buttonLayoutLazy = {
        "Normal" : DD_PLUGIN_STYLE_DELICIOUS,
        "Compact" : DD_PLUGIN_STYLE_DELICIOUS_COMPACT
    )
    
    def DD_Delicious() {
        
        self.option_append_type = self.OPTION_APPEND_TYPE
        self.option_button_design = self.OPTION_BUTTON_DESIGN
        self.option_button_weight = self.OPTION_BUTTON_WEIGHT
        self.option_ajax_left_float = self.OPTION_AJAX_LEFT_FLOAT
        self.option_lazy_load = self.OPTION_LAZY_LOAD
        
        self.baseURL_lazy = self.BASEURL_LAZY
        self.baseURL_lazy_script = self.BASEURL_LAZY_SCRIPT
        self.scheduler_lazy_script = self.SCHEDULER_LAZY_SCRIPT
        self.scheduler_lazy_timer = self.SCHEDULER_LAZY_TIMER
        
        self.button_weight_value = self.DEFAULT_BUTTON_WEIGHT
        
         self.BaseDD(self.NAME, self.URL_WEBSITE, self.URL_API, self.BASEURL)
    }  

    def constructNormalURL(url, title,button, postId):
        
        count = ''
        shareUrl = urlencode(url)
        deliciousStats = json_decode(file_get_contents('http:#feeds.delicious.com/v2/json/urlinfo/data?url='.shareUrl))
        
        if(!empty(deliciousStats)):
            if(deliciousStats->total_posts == 0) {
                count = '0'
            } elseif(deliciousStats->total_posts == 1) {
                count = '1'
            } else {
                count = deliciousStats->total_posts
            }
        }else{
            count = '0'
        }
        
        finalURL = self.baseURL
        finalURL = str_replace(VOTE_BUTTON_DESIGN,self.getButtonDesign(button),finalURL)
        finalURL = str_replace(VOTE_TITLE,title,finalURL)
        finalURL = str_replace(VOTE_URL,url,finalURL)
        finalURL = str_replace(self.SAVED_COUNT,count,finalURL)
        
        self.finalURL = finalURL
    }
   
    def constructLazyLoadURL(url, title,button, postId):
        
        finalURL_lazy = self.baseURL_lazy
        finalURL_lazy = str_replace(VOTE_BUTTON_DESIGN,self.getButtonDesignLazy(button),finalURL_lazy)
        finalURL_lazy = str_replace(VOTE_TITLE,title,finalURL_lazy)
        finalURL_lazy = str_replace(VOTE_URL,url,finalURL_lazy)
        finalURL_lazy = str_replace(POST_ID,postId,finalURL_lazy)
        #add new line
        finalURL_lazy = str_replace(self.SAVED_COUNT,'',finalURL_lazy)
        self.finalURL_lazy = finalURL_lazy
        
        finalURL_lazy_script = self.baseURL_lazy_script
        finalURL_lazy_script = str_replace(VOTE_BUTTON_DESIGN_LAZY_WIDTH,self.getButtonDesignLazyWidth(button),finalURL_lazy_script)
        finalURL_lazy_script = str_replace(VOTE_BUTTON_DESIGN_LAZY_HEIGHT,self.getButtonDesignLazyHeight(button),finalURL_lazy_script)
        finalURL_lazy_script = str_replace(VOTE_BUTTON_DESIGN,self.getButtonDesignLazy(button),finalURL_lazy_script)
        finalURL_lazy_script = str_replace(VOTE_TITLE,title,finalURL_lazy_script)
        finalURL_lazy_script = str_replace(VOTE_URL,url,finalURL_lazy_script)
        finalURL_lazy_script = str_replace(POST_ID,postId,finalURL_lazy_script)
        self.finalURL_lazy_script = finalURL_lazy_script
        
        final_scheduler_lazy_script = self.scheduler_lazy_script
        final_scheduler_lazy_script = str_replace(SCHEDULER_TIMER,self.scheduler_lazy_timer,final_scheduler_lazy_script)
        final_scheduler_lazy_script = str_replace(POST_ID,postId,final_scheduler_lazy_script)
        self.final_scheduler_lazy_script =  final_scheduler_lazy_script
    }
}

/******************************************************************************************
 * 
 * http:#www.stumbleupon.com
 * 
 */
class DD_StumbleUpon (BaseDD):
    
    NAME = "Stumbleupon"
    URL_WEBSITE = "http:#www.stumbleupon.com"
    URL_API = "http:#www.stumbleupon.com/badges/"
    BASEURL = "<script src='http:#www.stumbleupon.com/hostedbadge.php?s=VOTE_BUTTON_DESIGN&ampr=VOTE_URL'></script>"
    DEFAULT_BUTTON_WEIGHT = "97"
    
    OPTION_APPEND_TYPE = "dd_stumbleupon_appendType"
    OPTION_BUTTON_DESIGN = "dd_stumbleupon_buttonDesign"
    OPTION_BUTTON_WEIGHT = "dd_stumbleupon_button_weight"
    OPTION_AJAX_LEFT_FLOAT = "dd_stumbleupon_ajax_left_float"
    OPTION_LAZY_LOAD = "dd_stumbleupon_lazy_load"

    islazyLoadAvailable = False
    
    buttonLayout = {
        "Normal" : "5",
        "Compact" : "1"
    )
    
    def DD_StumbleUpon() {
        
        self.option_append_type = self.OPTION_APPEND_TYPE
        self.option_button_design = self.OPTION_BUTTON_DESIGN
        self.option_button_weight = self.OPTION_BUTTON_WEIGHT
        self.option_ajax_left_float = self.OPTION_AJAX_LEFT_FLOAT
        self.option_lazy_load = self.OPTION_LAZY_LOAD
        
        self.button_weight_value = self.DEFAULT_BUTTON_WEIGHT
        
         self.BaseDD(self.NAME, self.URL_WEBSITE, self.URL_API, self.BASEURL)

/******************************************************************************************
 * 
 * http:#buzz.yahoo.com
 * 
 */
class DD_YBuzz (BaseDD):

    NAME = "Yahoo Buzz"
    URL_WEBSITE = "http:#buzz.yahoo.com"
    URL_API = "http:#buzz.yahoo.com/buttons"
    DEFAULT_BUTTON_WEIGHT = "90"
    
    BASEURL = "<script type='text/javascript'>yahooBuzzArticleHeadline="VOTE_TITLE"yahooBuzzArticleId="VOTE_URL"</script><script type='text/javascript' src='http:#d.yimg.com/ds/badge2.js' badgetype='VOTE_BUTTON_DESIGN'></script>"
    
    OPTION_APPEND_TYPE = "dd_ybuzz_appendType"
    OPTION_BUTTON_DESIGN = "dd_ybuzz_buttonDesign"
    OPTION_BUTTON_WEIGHT = "dd_ybuzz_button_weight"
    OPTION_AJAX_LEFT_FLOAT = "dd_ybuzz_ajax_left_float"
    OPTION_LAZY_LOAD = "dd_ybuzz_lazy_load"
    
    islazyLoadAvailable = False
    
    buttonLayout = {
        "Normal" : "square",
        "Compact" : "small-votes",
        "Compact_Text" : "text-votes"
    )
    
    isEncodeRequired = False
    
    def DD_YBuzz() {
        
        self.option_append_type = self.OPTION_APPEND_TYPE
        self.option_button_design = self.OPTION_BUTTON_DESIGN
        self.option_button_weight = self.OPTION_BUTTON_WEIGHT
        self.option_ajax_left_float = self.OPTION_AJAX_LEFT_FLOAT
        self.option_lazy_load = self.OPTION_LAZY_LOAD
        
        self.button_weight_value = self.DEFAULT_BUTTON_WEIGHT
        
         self.BaseDD(self.NAME, self.URL_WEBSITE, self.URL_API, self.BASEURL)
    } 
    
}

/******************************************************************************************
 * 
 * http:#www.blogengage.com
 * 
 */
class DD_BlogEngage (BaseDD):

    NAME = "BlogEngage"
    URL_WEBSITE = "http:#www.blogengage.com"
    URL_API = "http:#www.blogengage.com/profile_promo.php"
    DEFAULT_BUTTON_WEIGHT = "84"
    
    BASEURL = "<script type='text/javascript'>submit_url = 'VOTE_URL'</script><script src='http:#blogengage.com/evb/VOTE_BUTTON_DESIGN'></script>"
  
    OPTION_APPEND_TYPE = "dd_blogengage_appendType"
    OPTION_BUTTON_DESIGN = "dd_blogengage_buttonDesign"
    OPTION_BUTTON_WEIGHT = "dd_blogengage_button_weight"
    OPTION_AJAX_LEFT_FLOAT = "dd_blogengage_ajax_left_float"
    OPTION_LAZY_LOAD = "dd_blogengage_lazy_load"
    
    islazyLoadAvailable = False
    isEncodeRequired = False
    
    buttonLayout = {
        "Normal" : "button4.php"
    )
    
    def DD_BlogEngage() {
        
        self.option_append_type = self.OPTION_APPEND_TYPE
        self.option_button_design = self.OPTION_BUTTON_DESIGN
        self.option_button_weight = self.OPTION_BUTTON_WEIGHT
        self.option_ajax_left_float = self.OPTION_AJAX_LEFT_FLOAT
        self.option_lazy_load = self.OPTION_LAZY_LOAD
        
        self.button_weight_value = self.DEFAULT_BUTTON_WEIGHT
        
         self.BaseDD(self.NAME, self.URL_WEBSITE, self.URL_API, self.BASEURL)
    } 
    
}  

/******************************************************************************************
 * 
 * http:#www.designbump.com
 * 
 */
class DD_DesignBump (BaseDD):
    
    NAME = "DesignBump"
    URL_WEBSITE = "http:#www.designbump.com"
    URL_API = "http:#designbump.com/content/evb"
    DEFAULT_BUTTON_WEIGHT = "87"

    BASEURL = "<script type='text/javascript'>url_site='VOTE_URL' </script> <script src='http:#designbump.com/sites/all/modules/drigg_external/js/button.js' type='text/javascript'></script>"
    
    OPTION_APPEND_TYPE = "dd_designbump_appendType"
    OPTION_BUTTON_DESIGN = "dd_designbump_buttonDesign"
    OPTION_BUTTON_WEIGHT = "dd_designbump_button_weight"
    OPTION_AJAX_LEFT_FLOAT = "dd_designbump_ajax_left_float"
    OPTION_LAZY_LOAD = "dd_designbump_lazy_load"
    
    islazyLoadAvailable = False
    isEncodeRequired = False
    
    buttonLayout = {
        "Normal" : "Normal"
    )
    
    def DD_DesignBump() {
        
        self.option_append_type = self.OPTION_APPEND_TYPE
        self.option_button_design = self.OPTION_BUTTON_DESIGN
        self.option_button_weight = self.OPTION_BUTTON_WEIGHT
        self.option_ajax_left_float = self.OPTION_AJAX_LEFT_FLOAT
        self.option_lazy_load = self.OPTION_LAZY_LOAD
        self.button_weight_value = self.DEFAULT_BUTTON_WEIGHT
        
        self.BaseDD(self.NAME, self.URL_WEBSITE, self.URL_API, self.BASEURL)

    } 
    
}

/******************************************************************************************
 * 
 * http:#www.thewebblend.com
 * 
 */
class DD_TheWebBlend (BaseDD):

    NAME = "TheWebBlend"
    URL_WEBSITE = "http:#www.thewebblend.com"
    URL_API = "http:#thewebblend.com/tools/vote"
    DEFAULT_BUTTON_WEIGHT = "85"

    BASEURL = "<script type='text/javascript'>url_site='VOTE_URL' VOTE_BUTTON_DESIGN</script><script src='http:#thewebblend.com/sites/all/modules/drigg_external/js/button.js' type='text/javascript'></script>"
    
    OPTION_APPEND_TYPE = "dd_webblend_appendType"
    OPTION_BUTTON_DESIGN = "dd_webblend_buttonDesign"
    OPTION_BUTTON_WEIGHT = "dd_webblend_button_weight"
    OPTION_AJAX_LEFT_FLOAT = "dd_webblend_ajax_left_float"
    OPTION_LAZY_LOAD = "dd_webblend_lazy_load"
    
    islazyLoadAvailable = False
    isEncodeRequired = False
    
    buttonLayout = {
        "Normal" : "",
        "Compact" : "badge_size='compact'"
    )
    
    def DD_TheWebBlend() {
        
        self.option_append_type = self.OPTION_APPEND_TYPE
        self.option_button_design = self.OPTION_BUTTON_DESIGN
        self.option_button_weight = self.OPTION_BUTTON_WEIGHT
        self.option_ajax_left_float = self.OPTION_AJAX_LEFT_FLOAT
        self.option_lazy_load = self.OPTION_LAZY_LOAD
        
        self.button_weight_value = self.DEFAULT_BUTTON_WEIGHT
        
        self.BaseDD(self.NAME, self.URL_WEBSITE, self.URL_API, self.BASEURL)
    }    
}

/******************************************************************************************
 * 
 * http:#www.tweetmeme.com/
 * 
 */
class DD_TweetMeme (BaseDD):
    
    NAME = "TweetMeme"
    URL_WEBSITE = "http:#www.tweetmeme.com/"
    URL_API = "http:#wordpress.org/extend/plugins/tweetmeme/"
    DEFAULT_BUTTON_WEIGHT = "97"
    
    BASEURL ="<iframe src='http:#api.tweetmeme.com/button.js?url=VOTE_URL&source=VOTE_SOURCE&service=VOTE_SERVICE_NAME&service_api=VOTE_SERVICE_API&style=VOTE_BUTTON_DESIGN frameborder='0' scrolling='no'></iframe>"
    OPTION_APPEND_TYPE = "dd_tweetmeme_appendType"
    OPTION_BUTTON_DESIGN = "dd_tweetmeme_buttonDesign"
    OPTION_BUTTON_WEIGHT = "dd_tweetmeme_button_weight"
    OPTION_AJAX_LEFT_FLOAT = "dd_tweetmeme_ajax_left_float"
    OPTION_LAZY_LOAD = "dd_tweetmeme_lazy_load"
    
    BASEURL_LAZY = "<div class='dd-tweetmeme-ajax-load dd-tweetmeme-POST_ID'></div><iframe class='DD_TWEETMEME_AJAX_POST_ID' src='' height='0' width='0' scrolling='no' frameborder='0'></iframe>"
    BASEURL_LAZY_SCRIPT = " function loadTweetMeme_POST_ID(): jQuery(document).ready(function(\) { \('.dd-tweetmeme-POST_ID').remove()\('.DD_TWEETMEME_AJAX_POST_ID').attr('width','VOTE_BUTTON_DESIGN_LAZY_WIDTH')\('.DD_TWEETMEME_AJAX_POST_ID').attr('height','VOTE_BUTTON_DESIGN_LAZY_HEIGHT')\('.DD_TWEETMEME_AJAX_POST_ID').attr('src','http:#api.tweetmeme.com/button.js?url=VOTE_URL&source=VOTE_SOURCE&style=VOTE_BUTTON_DESIGN&service=VOTE_SERVICE_NAME&service_api=VOTE_SERVICE_API') }) }"
    SCHEDULER_LAZY_SCRIPT = "window.setTimeout('loadTweetMeme_POST_ID()',SCHEDULER_TIMER)"
    SCHEDULER_LAZY_TIMER = "1000"
    
    buttonLayout = {
        "Normal" : "normal' height='61' width='50'",
        "Compact" : "compact' height='20' width='90'"
    )
    
    buttonLayoutLazy = {
        "Normal" : "normal",
        "Compact" : "compact"
    )
    
    buttonLayoutLazyWidth = {
        "Normal" : "50",
        "Compact" : "90"
    )
    
    buttonLayoutLazyHeight = {
        "Normal" : "61",
        "Compact" : "20"
    )
    
    isEncodeRequired = False
     
    VOTE_SOURCE = "VOTE_SOURCE"
    VOTE_SERVICE_NAME = "VOTE_SERVICE_NAME"
    VOTE_SERVICE_API = "VOTE_SERVICE_API"
    
    def DD_TweetMeme() {
        
        self.option_append_type = self.OPTION_APPEND_TYPE
        self.option_button_design = self.OPTION_BUTTON_DESIGN
        self.option_button_weight = self.OPTION_BUTTON_WEIGHT
        self.option_ajax_left_float = self.OPTION_AJAX_LEFT_FLOAT
        self.option_lazy_load = self.OPTION_LAZY_LOAD
        
        self.baseURL_lazy = self.BASEURL_LAZY
        self.baseURL_lazy_script = self.BASEURL_LAZY_SCRIPT
        self.scheduler_lazy_script = self.SCHEDULER_LAZY_SCRIPT
        self.scheduler_lazy_timer = self.SCHEDULER_LAZY_TIMER

        self.button_weight_value = self.DEFAULT_BUTTON_WEIGHT
        
        self.BaseDD(self.NAME, self.URL_WEBSITE, self.URL_API, self.BASEURL)
    } 
    
    def constructURL(url, title,button, postId, lazy, globalcfg = ''):
        
         if(self.isEncodeRequired):
             title = quote(title)
            url = quote(url)
         }
         
         source = ''
         service = ''
         serviceapi = ''
         
         if(globalcfg!=''):
             source = globalcfg[DD_GLOBAL_TWEETMEME_OPTION][DD_GLOBAL_TWEETMEME_OPTION_SOURCE] 
             service = globalcfg[DD_GLOBAL_TWEETMEME_OPTION][DD_GLOBAL_TWEETMEME_OPTION_SERVICE]
             serviceapi = globalcfg[DD_GLOBAL_TWEETMEME_OPTION][DD_GLOBAL_TWEETMEME_OPTION_SERVICE_API]
         }

        if(lazy==DD_EMPTY_VALUE):

            self.baseURL = str_replace(VOTE_SOURCE,source,self.baseURL)
            self.baseURL = str_replace(VOTE_SERVICE_NAME,service,self.baseURL)
            self.baseURL = str_replace(VOTE_SERVICE_API,serviceapi,self.baseURL)
        
            self.constructNormalURL(url, title,button, postId)
            
        }else{

            self.baseURL_lazy_script = str_replace(VOTE_SOURCE,source,self.baseURL_lazy_script)
            self.baseURL_lazy_script = str_replace(VOTE_SERVICE_NAME,service,self.baseURL_lazy_script)
            self.baseURL_lazy_script = str_replace(VOTE_SERVICE_API,serviceapi,self.baseURL_lazy_script)
        
            self.constructLazyLoadURL(url, title,button, postId)
        }
        

/******************************************************************************************
 * 
 * http:#www.topsy.com
 * 
 */
class DD_Topsy (BaseDD):
    
    NAME = "Topsy"
    URL_WEBSITE = "http:#www.topsy.com"
    URL_API = "http:#labs.topsy.com/button/retweet-button/"
    DEFAULT_BUTTON_WEIGHT = "96"
    
    BASEURL = "<script type="text/javascript" src="http:#cdn.topsy.com/topsy.js?init=topsyWidgetCreator"></script><div class="topsy_widget_data"><!--{"url":"VOTE_URL","style":"VOTE_BUTTON_DESIGN","theme":"VOTE_THEME","nick":"VOTE_SOURCE"}--></div>"

    OPTION_APPEND_TYPE = "dd_topsy_appendType"
    OPTION_BUTTON_DESIGN = "dd_topsy_buttonDesign"
    OPTION_BUTTON_WEIGHT = "dd_topsy_button_weight"
    OPTION_AJAX_LEFT_FLOAT = "dd_topsy_ajax_left_float"
    OPTION_LAZY_LOAD = "dd_topsy_lazy_load"

    VOTE_SOURCE = "VOTE_SOURCE"
    VOTE_THEME = "VOTE_THEME"
    
    islazyLoadAvailable = False
    isEncodeRequired = False
    
    buttonLayout = {
        "Normal" : "big",
        "Compact" : "compact"
    )
    
    def DD_Topsy() {
        
        self.option_append_type = self.OPTION_APPEND_TYPE
        self.option_button_design = self.OPTION_BUTTON_DESIGN
        self.option_button_weight = self.OPTION_BUTTON_WEIGHT
        self.option_ajax_left_float = self.OPTION_AJAX_LEFT_FLOAT
        self.option_lazy_load = self.OPTION_LAZY_LOAD

        self.button_weight_value = self.DEFAULT_BUTTON_WEIGHT
        
        self.BaseDD(self.NAME, self.URL_WEBSITE, self.URL_API, self.BASEURL)
        
    } 
    
    def constructURL(url, title,button, postId, lazy, globalcfg = ''):

        if(self.isEncodeRequired):
             title = quote(title)
            url = quote(url)
         }
         
         source = ''
         theme = ''
         
         if(globalcfg!=''):
             source = globalcfg[DD_GLOBAL_TOPSY_OPTION][DD_GLOBAL_TOPSY_OPTION_SOURCE] 
             theme = globalcfg[DD_GLOBAL_TOPSY_OPTION][DD_GLOBAL_TOPSY_OPTION_THEME]
         }
         
        finalURL = ''
        finalURL = str_replace(VOTE_BUTTON_DESIGN,self.getButtonDesign(button),self.baseURL)
        finalURL = str_replace(VOTE_URL,url,finalURL)
        finalURL = str_replace(VOTE_SOURCE,source,finalURL)
        finalURL = str_replace(VOTE_THEME,theme,finalURL)
    
        self.finalURL = finalURL



class DD_Comments (BaseDD):

    NAME = "Comments"
    URL_WEBSITE = "http:#none"
    URL_API = "http:#none"
    DEFAULT_BUTTON_WEIGHT = "88"
    
    BASEURL = "<div id='dd_comments'><a class='clcount' href=VOTE_URL><span class='ctotal'>COMMENTS_COUNT</span></a><a class='clink' href=VOTE_URL></a></div>"
    
    OPTION_APPEND_TYPE = "dd_comments_appendType"
    OPTION_BUTTON_DESIGN = "dd_comments_buttonDesign"
    OPTION_BUTTON_WEIGHT = "dd_comments_button_weight"
    OPTION_AJAX_LEFT_FLOAT = "dd_comments_ajax_left_float"
    OPTION_LAZY_LOAD = "dd_comments_lazy_load"
    
    COMMENTS_COUNT = "COMMENTS_COUNT"
    COMMENTS_RESPONSE_ID = "#respond"
    
    islazyLoadAvailable = False
    
    buttonLayout = {
        "Normal" : "Normal",
    )
    
    def DD_Comments() {
        
        self.option_append_type = self.OPTION_APPEND_TYPE
        self.option_button_design = self.OPTION_BUTTON_DESIGN
        self.option_button_weight = self.OPTION_BUTTON_WEIGHT
        self.option_ajax_left_float = self.OPTION_AJAX_LEFT_FLOAT
        self.option_lazy_load = self.OPTION_LAZY_LOAD
        
        self.button_weight_value = self.DEFAULT_BUTTON_WEIGHT
        
        self.BaseDD(self.NAME, self.URL_WEBSITE, self.URL_API, self.BASEURL)
        
    }     
    
    def constructURL(url, title,button, postId, lazy, globalcfg = '', commentcount = ''):
        result = ''
        
        url = url . self.COMMENTS_RESPONSE_ID
        result = str_replace(VOTE_URL,url,self.baseURL)
        result = str_replace(self.COMMENTS_COUNT,commentcount,result)
        
        self.finalURL = result

class DD_Serpd (BaseDD):
    
    NAME = "Serpd"
    URL_WEBSITE = "http:#www.serpd.com"
    URL_API = "http:#www.serpd.com/widgets/"
    BASEURL = "<script type="text/javascript">submit_url = "VOTE_URL"</script><script type="text/javascript" src="http:#www.serpd.com/index.php?page=evb"></script>"
    
    OPTION_APPEND_TYPE = "dd_serpd_appendType"
    OPTION_BUTTON_DESIGN = "dd_serpd_buttonDesign"
    OPTION_BUTTON_WEIGHT = "dd_serpd_button_weight"
    OPTION_AJAX_LEFT_FLOAT = "dd_serpd_ajax_left_float"
    OPTION_LAZY_LOAD = "dd_serpd_lazy_load"
    
    DEFAULT_BUTTON_WEIGHT = "86"
    
    islazyLoadAvailable = False
    isEncodeRequired = False
    
    buttonLayout = {
        "Normal" : "",
    )
    
    def DD_Serpd() {
        
        self.option_append_type = self.OPTION_APPEND_TYPE
        self.option_button_design = self.OPTION_BUTTON_DESIGN
        self.option_button_weight = self.OPTION_BUTTON_WEIGHT
        self.option_ajax_left_float = self.OPTION_AJAX_LEFT_FLOAT
        self.option_lazy_load = self.OPTION_LAZY_LOAD
        
        self.button_weight_value = self.DEFAULT_BUTTON_WEIGHT
        
        self.BaseDD(self.NAME, self.URL_WEBSITE, self.URL_API, self.BASEURL)
    }    
}"""

DIGGDIGG_CLASSES = [DD_Twitter, DD_FbLike_XFBML, DD_FbShare]

DiggDiggVocabulary = SimpleVocabulary([
    SimpleTerm(d.NAME, d.NAME, unicode(d.NAME)) for d in DIGGDIGG_CLASSES
])
