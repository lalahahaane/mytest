#python-social-auth运作流程#

>原文[http://www.leehodgkinson.com/blog/a-stroll-through-the-python-social-auth-code/](http://www.leehodgkinson.com/blog/a-stroll-through-the-python-social-auth-code/ "这里")
>车溪译

  本文描述了利用python-social-auth实现第三方登录的相当冗长曲折的流程，重点是什么？就我个人而言，我发现理解python-social-auth如何运作的最好的方法就是看懂代码。如果不出意外，数月后当一切已经被我遗忘，这篇博客中的笔记能提供一些参考。出于演示考虑，我将在下文中以django中google-plus的登录流程为例子。

##开始##

像所有在django里的东西一样，我们进入整个流程的入口就在`urls.py`。python-social-auth(下文中我们简称“pas”)是从django-social-auth发展而来，所以在代码中当然包含一个django app。这个app 就在`social/apps/django_app/`(你也能在其他框架中使用pas,比如可以在tornado中使用的pas)。pas最了不起的特征就是，这种方式编写的代码，能十分容易得通过写一个新的"strategy"(战略),"storage"(存储)和"backend"(后端)而适用于到不同的平台和认证后端。咋一看，这也为代码添加了几分神秘感。

在这个app里,首先把你的文本编辑器切换到`urls.py`文件里。当用户开始google-plus登录过程它们直接指向这个url `social/login/google-plus/`(不用管pas里的urls文件是什么，它相对于你的django主urls文件)。“google-plus”这个字符串会被psa里的`urls.py`中的**[正则表达式捕获组](https://docs.djangoproject.com/en/dev/topics/http/urls/#named-groups "正则表达式捕获组 regex capture group ")**捕获然后传递给视图(app里的`views.py`)里叫"auth"的（tips:这个url的指定名称为“begin”，它能正常的像django中其他反向访问一样，可以利用反向解析django [reverse](https://docs.djangoproject.com/en/dev/ref/urlresolvers/#reverse "reverse")解析"social:begin"这个url，记住psa的命名空间namespace是“social”）。

因此，我们接下来看在psa的`views.py`视图里的`auth`函数。第一眼看这个函数并没有干很多事而是调用了另一些函数。捕获到的“google-plus”字符串将会和request一起当做`backend`的参数，然后我们调用了函数`do_auth`(`social/actions.py`),backend和重定向名`redirect_name`(字段的名称指向登录流程结束后重定向到哪里,这可以通过查询字符串query string传递)。通常这个字段名称是"next",并且它可以通过像`?next=/someurl/&`这样的查询字符串query string传递。我们将看到，这个字段的值取决于用户最终在整个注册登录流程完成后接着到哪。

关于视图最有意思的是`psa`的装饰器。用户可以通过设置他们的django `settings.py`里的`URL_NAMESPACE`变量来定义`NAMESPACE`参数，但是默认的NAMESPACE参数是字符串“social”,所以我们发现我们把这个装饰器叫做`@psa('social:'complete)`。这个参数是django为psa的完成url取的名字，换句话说，`reverse("social:complete", args=("google-plus",))`能够得到（相对）`url social/complete/google-plus`。这就是我们要告诉google回返的重定向url(不要对这个重定向感到疑惑，上文中我们讨论了用户完成整个流程后会重定向到某个地方)。

tips:你可以实际设置`SOCIAL_AUTH_URL_NAMESPACE = ...`,所有psa的settings都以"SOCIAL_AUTH"开始。源代码中，`utils.py`里的`setting_name`函数加入以"SOCIAL_AUTH"为前缀的设定。
我们找到`social/apps/django/utils.py`看看psa的装饰器如何定义和工作的。

##psa装饰器##

psa装饰器定义如下：

    from social.apps.django_app.utils import psa

	def psa(redirect_uri=None, load_strategy=load_strategy):
    	def decorator(func):
    		@wraps(func)
    		def wrapper(request, backend, *args, **kwargs):
		    	uri = redirect_uri
		    	if uri and not uri.startswith('/'):
		    		uri = reverse(redirect_uri, args=(backend,))

	            request.social_strategy = load_strategy(request)
	            # backward compatibility in attribute name, only if not already
	            # defined
	            if not hasattr(request, 'strategy'):
	                request.strategy = request.social_strategy

	            try:
	                request.backend = load_backend(request.social_strategy,
	                                               backend, uri)
	            except MissingBackend:
	                 raise Http404('Backend not found')
	            return func(request, backend, *args, **kwargs)
	         return wrapper
	    return decorator

这是一段令人相当眩晕的代码（函数里包含函数然后又包含。。。），其实它实际上是一个普通的带参数函数装饰器的院子，如果你曾经理解了他们中的一个，你也能理解其他的类似代码。psa wrapper（意思为：包装、包裹）可以构造和返回装饰器（线索就在名字）。现在是修改python 101 decorators的好时机！[python decorators 101](http://www.jarrodctaylor.com/posts/Python_Decorators_101/ "Python Decorators 101")

> 旁白：在编写的装饰器函数里面，你可以看到这句`@wraps(func)`,因此你需要理解函数工具`wraps`的作用。可以参考[这里](http://stackoverflow.com/questions/308999/what-does-functools-wraps-do "wraps的使用")帮助理解，简而言之`wraps`的作用就是解决func丢失某些函数信息，比如它的docstring,`__name__`属性,携带参数个数等，当使用wrapper函数这些丢失的信息可以由装饰器函数返回。如果这些还不太明白，看看这个我推荐的非常通俗易懂的stack-exchange[链接](http://stackoverflow.com/questions/308999/what-does-functools-wraps-do "what-does-functools-wraps-do")。理解wraps的作用对了解psa如何工作影响并不太大，所以如果你仍然不明白它，不用担心你仍然能继续。。。

如果你记性不错的话，装饰器能充当函数的作用，这里我叫`func`,它用来构造和返回另一个函数，这里叫wrapper包裹(它包裹带额外的代码的函数)。wrapper函数返回和代替原来的函数。我用下面的符号表示：

     @decorator
     def func(x):
    	 print x

上面的是下面这两行代码的简写方式

    func = decorator(func)   # the wrapper function has now replaced func
     = wrapper

它们完全相等。因此在psa里，我们使用的函数上面的装饰叫做“decorator”，它被用于返回函数，并且用名为"wrapper"的函数代替。

现在忘记wrapper的实际作用，这里你可能会问的第一个问题（特别是如果以前你只在python中使用过基本的装饰器）是“为什么我们看到一个装饰器在另一个装饰器里面？”。为什么我们不像这样定义装饰器

    def decorator(func):
    	@wraps(func)
    	def wrapper(request, backend, *args, **kwargs):
		    .
		    .
		    .
	    return wrapper
然后这样使用

    @decorator('{0}:complete'.format(NAMESPACE))
    def auth(request, backend):
	    .
	    .

答案就是事实上我们想要一个能够携带参数的函数装饰器。所有植入函数的额外的几层能够允许我们在装饰器里加redirect_uri参数（google返回的），而不是仅仅返回一般意义上的装饰器（看[ Decorator functions with Decorator arguments](http://www.artima.com/weblogs/viewpost.jsp?thread=240845 "Decorators without Arguments")）带参数的装饰器能够带着一个函数并且返回另一个函数，换句话说，它能返回一个标准的装饰器。用代码表示就是：

	def decorator_with_args(argument):
        def real_decorator(function):
		    def wrapper(*args, **kwargs):
		    .
		    .
		    return wrapper
     	return real_decorator
简易的使用方法是：

    @decorator_with_args(arg)
    def func(*args, **kwargs):
    	pass

可以把它解释成：

    func = decorator_with_args(arg)(func)
    	 = real_decorator(func)         # which is equal to wrapper

此时，arg在the real_decorator内可以使用了，但是除此之外我们继续使用通常的装饰器。总的概括，**psa是一个”带参数的函数装饰器“**，它代替了这样的函数，在运行最初的代码之前运行预先编码的函数。it replaces the function it acts on by another function that runs some pre-code before running the original code of the function it replaced.
##Wrapper包裹

理解了所有这些之后，我们回到wrapper这个话题，这个替代性的函数"wrapper"实际上是干什么用的？首先我们明白它能像函数一样使用参数和关键字参数。它能顺带取出`request`和`backend`参数以及通过 `*args, **kwargs`携带剩下的args and kwargs 。

我们一开始在psa里叫redirect_uri的参数（记住在本文的django里google-plus利用"social:complete字符串反向解析获取整个google-plus auth链接）可以反向解析。

    uri = reverse(redirect_uri, args=(backend,))

所以uri从字面上看有点像 (相对于你的其他django urls) `social/complete/google-plus`。它将最终作为callback uri回调uri传递给
下一步`wrapper` 载入相应的strategy (看下面的旁白), and sets the `social_strategy` attribute of the request with the result. 这和backend很相似. 最终, 像大多数装饰器一样它返回原始函数the original function, `func(request, backend, *args, **kwargs)`.

>
旁白: 但是什么是"strategy"?在本质上一个strategy是psa需要的为特定平台执行的方法的集合, e.g. django。因此我们可以这样认为，psa需要构造一条绝对的uri, 我们可以知道这通过 `request.build_absolute_uri(path)`实现这个需求, so the Django strategy has a "build_absolute_uri" function that does it just that way, whereas in another platform, webpy, we have to implement `build_absoluite_uri` so it's specific to that platform: `web.ctx.protocol + '://' + web.ctx.host + path`.像这样有针对每个平台的stategies,拥有通用性的代码主体意味着psa的代码主干能适应各种平台，比如 like django, tornado, webpy ....简单的说，通过设置你的 strategy能使你构建绝对 uri , 然后就可以使用 `strategy.build_absolute_uri('/somepath')`, 根据你的平台执行对应的函数。 Very nice， 相似的, "storage" 这个概念是一种允许代码适应不同平台而不用担心针对特定平台细节的明智方法 (e.g. 现在 `storage.user.create_user` 可以解释为django中的`UserSocialAuth.create_user(...)` , 这就变成了使用 django orm的一个django model)

##load_strategy and load backend

从字面意思上理解. 用`social.strategies.utils`里的 `get_strategy`函数  :


    def get_strategy(strategy, storage, *args, **kwargs):
	    Strategy = module_member(strategy)
	    Storage = module_member(storage)
	    return Strategy(Storage, *args, **kwargs)

在这里`'social.strategies.django_strategy.DjangoStrategy'`这一条字符串默认`strategy` 的参数是 `STRATEGY` (如果不是这样的话，那么你已经通过设置你的 django `settings.py`里的`SOCIAL_AUTH_STRATEGY`来改变它 ),同样的`social.apps.django_app.default.models.DjangoStorage`这一条字符串默认storage 的参数是 `STORAGE`. Once imported the Strategy is initialized with the Storage (this initializiation just involves setting the strategy attribute of the stoage to the storage we passed in) and then returned.
As for load backend: you guessed it, it just initializes and returns the backend. `AUTHENTICAON_BACKEND `is set by the user in `settings.py` as a list of backends to try in order, and this in turn sets the `BACKEND` parameter in `apps/django_apps/utils`. The `load_backend` function takes the strategy we just loaded, the backend which we parsed from the `do_auth` view ('google-plus' for us), and the redirect uri that we constructed, called `uri`. The `get_backend` function takes this `BACKEND` list, plus the one we actually want `backend` ("google-plus"), and returns the actual appropriate Backend class. Finally, we initialize this Backend by setting the strategy attribute to the strategy object and the `redirect_uri` attr to redirect uri we have for the callback, and it is returned.

##actions/do_auth.py

现在把绕了几个圈的psa装饰器放一边, 我们继续回到google- plus 登录流程的`actions.py` 中的`do_auth`
数据可以从request object(QueryDict in django)中获取 :

    data = backend.strategy.request_data(merge=False)

Using the django strategy, the `request_data` function is implemented in a way that simply checks if the request method is 'GET' or 'POST' and returns either the `request.GET` or `request.POST` parameters accordingly. The exception being when merge is enabled, in which the data from GET and POST is `merged` and returned.
Some of this data is then saved into the session.
`backend.setting` means get the setting using


    return self.strategy.setting(name, default=default, backend=self)

i.e. passing the current backend to get the setting within the argument 'name' (see `strategies/base.py`), the inclusion of the backend means that instead of looking for `SOCIAL_AUTH_FIELDS_STORED_IN_SESSION` we actually look for a backend specific setting, `SOCIAL_AUTH_GOOGLE_PLUS_FIELDS_STORED_IN_SESSION`. This is all done with the `setting_name` function (which is also the function responsible for prefixing all the settings with "SOCIAL_AUTH"). The function `get_setting` will be the strategy specific way of getting settings that must be implemented per platform, e.g. in `django_stretegy.py`.
In other words, a user can set `SOCIAL_AUTH_GOOGLE_PLUS_FIELDS_STORED_IN_SESSION` in their django settings.py, and this will force psa to store in the session these fields and their associated data if they are present in the request data.
Next we look for the `redirect_name` (remember by default this is the string "next") in the data, if it's there grab its value and save it as `redirect_uri` (NB there is an important distinction to be made here; this `redirect_uri` is grabbed from the "next" parameter in the GET string on a request if present, e.g. "social/login/google-plus/?next=/after_the_signin_view&", and this is used to redirect the user to some URL when the entire sign-in flow is over. Earlier in the psa wrapper we saw that another `redirect_uri`, which for the `auth` view was a URL identified by the reverse of "social:complete", was used in `load_backend` when initializing the Backend to set the attribute redirect_uri of the backend. The latter will be used to pass to google during the auth request to callback to with the auth code)
If the user has opted in their settings to sanitze redirects, then this function tests the redirect uri grabbed from the next parameter in the query string, by making sure that 1) it's a valid uri 2) if the uri is absolute and has a hostname, this hostname matches what the hostname should be.
We then store this URI to session (again using the django strategy associated with the backend to make sure the appropriate session setting logic is ran). Session will now have a `next` key of the value of the `redirect_uri`.
Finally we run

    backend.start()

##backend.start()##

The start method is implemented in backends/base.py in the BaseAuth class, which is the parent class for the OAuthAuth class, which in turn is a parent to BaseOAuth2, which finally is a parent to GooglePlusAuth (along with BaseGoogleOAuth2API).
It's a very short method that runs like
Clean partial pipeline: we will discuss partial pipelines later, but for this just pops the key "partial_pipeline" from the session (see strategies/base.py)
Tests if backend uses a redirect: in backends/base.py this is a function that just returns True, and it is not overriden in oath.py or google.py, so the answer is yes, we do use a redirect.
Builds an auth_url: (see backends/oath.py and BaseOAuth2) First in the auth_url building comes the get_or_create_state. State is the OAuth state parameter that according to the spec can be passed to google and will be returned by google (it's useful for things like CSRF tokens to validate requests). For google-plus the STATE_PARAMETER and REDIRECT_STATE are both None (why?), so the state is always just set to None. The function auth_params contributes next, adding client_id and client_secret, and the response_type (which for us will be "code") It also sets the redirect_uri for google to callback to (ultimately using the redirect_uri attribute of the backend that the psa decorator set . Further we get scope arguments, ultimately this relies on get_scope of backends/google.py, and it adds any scopes the user has defined in settings.py to the default scopes (e.g. "https://www.googleapis.com/auth/userinfo.email" to grab a user's email). The auth_extra_arguments line parses extra authentication arguments the user may have given in settings.py with the AUTH_EXTRA_ARGUMENTS setting (e.g. you could use this setting to pass something like {'access_type': 'offline'}). Finally this dictionary of params is url encoded, and appended to the self.authorization_url(), which returns self.AUTHORIZATION_URL (see backends/oauth.py) and which for google-plus is defined:
AUTHORIZATION_URL = 'https://accounts.google.com/o/oauth2/auth'
Ultimately we have built an auth url that looks something like




    https://accounts.google.com/o/oauth2/auth?redirect_uri=http://example.com/account/social/complete/google-plus/&response_type=code&client_id=YOURCLIENTID&scope=YOURSCOPES&

which we redirect to with

    self.strategy.redirect(self.auth_url())

for which the django strategy ensures this redirect is translates it the appropriate django logic, i.e.

    from django.shortcuts import redirect
    def redirect(self, url):
    	return redirect(url)

##apps/django_app/views.py complete##

By virtue of setting our redirect_uri that we sent in auth requests GET params to Google, Google should callback to the reversal of "social:complete" after the users has signed in and consented, along with an "auth code".
The psa wrapper does its magic again, loading the request with the strategy, backend, and again setting the redirect uri to "social:complete" (i.e. we callback to the same view) ... and we call `do_complete`.

##do_complete##

The data is grabbed from the request, and we next call `user_is_authenticated(user)` . This function basically just calls the `is_authenticated()` method if available and returns the boolean result. The line

    user = is_authenticated and user or None

means if `is_authenticated` is True, the user object will be assigned to user, else the user will be assigned None (since if `is_authenticated` is False there will be no need to check the user obj for truth and python logic jumps to the second branch of the "or"). On the first login we expect the user object to be AnonymousUser and so here user is set to None.
Next we come to the partial_pipeline_data: this function pops the partial_pipeline var from the session, and if it exists calls

    partial = backend.strategy.session_get('partial_pipeline', None)
    idx, backend_name, xargs, xkwargs = \
    	backend.strategy.partial_from_session(partial)

(see `strategies/base.py` and then `pipeline/utils.py`).
We will come the pipelines and partial pipelines later, so for now do not worry too much about this. On the first pass, and if with no partial pipelines involved, the next step of the code will be backend.complete.

##backend.complete##

If not partial, we run `backend.complete`, which as `backends/base.py` shows, is just a proxy for `auth_complete(*args, **kwargs)` (see `backends/google.py`). We make sure if the access token is present the code param is present, else we raise an exception for missing param. We attempt to grab the access token (this won't be present on the first pass. The redirect uri is not used for callback by google at this stage, we just issue a simple request/response and the user is not sent off anywhere, but google requires the redirect uri as an extra security consistency check).
Assuming we don't have the access token yet we want to use our auth code to make an access token request:

	response = self.request_access_token(
                         self.ACCESS_TOKEN_URL,
                         data=self.auth_complete_params(),
                         headers=self.auth_headers(),
                         method=self.ACCESS_TOKEN_METHOD
                         )
where for `google-plus`:

	ACCESS_TOKEN_URL = 'https://accounts.google.com/o/oauth2/token'
	ACCESS_TOKEN_METHOD = 'POST'

the headers are (see `backends/oauth.py`)

	 {'Content-Type': 'application/x-www-form-urlencoded',
	   'Accept': 'application/json'}

the auth params are the same as those defined for BaseOAuth2 in oauth.py, but also include the access token should it exist, e.g.

 	{
        'grant_type': 'authorization_code',  # request auth code
        'code': self.data.get('code', ''),  # server response code
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': self.get_redirect_uri(state)  # will be social:complete again despite no actual callback occuring at this stage, inclusion is a consistency check for security.
    }
With those ingredients, we turn to the request_access_token code. In backends/oauth.py this is just a wrapper for get_json, and in backends/base.py we see this is just a wrapper for self.request(.....).json().
The request method (base.py) is nothing complicated, it just using python requests and the ingredients to actually make the request to google on the provided URL, with the provided method, headers etc...and does some Exception catching. Before returning the response, we call

	response.raise_for_status()

which just raises a HTTPError of the appropriate type if we get a non 200 response code, you can read more in the pyhon-requests docs.
After getting this JSON response, we check it for errors (we are back in backends/google.py auth_complete now), which involves calling process_error (see backends/oauth.py), which checks the response data for the 'error' key, and if it exists and has value 'denied' or 'access_denied' we raise the exception 'AuthCancled' (the user bailed on us) or if not just a simple AuthFailed.
If no errors, finally call do_auth with the access token (that we should now have if there were no errors) and the rest of the response

	return self.do_auth(response['access_token'], response=response,
                                 *args, **kwargs)

See backends/oauth.py for the do_auth code. It involves first using our access token to grab some user data (see backends/google.py BaseGoogleOAuth2API) ensuring we use the correct scope, e.g. https://www.googleapis.com/plus/v1/people/me)....remember get_json as we discussed above is just a request really but jsonified with .json() applied to response. In do_auth we add whatever user data we grabbed back to the response, and update the kwargs with the new response.
With this user info injected to the response and in turn the response injected to the kwargs, we run

 	self.strategy.authenticate(*args, **kwargs)

which for django just means using the usual django authenticate (from django.contriib.auth)

##Django authenticate##

This method (see `django/contrib/auth/__init__.py`) simply loops through the list of backends supplied in the django settings.py, trying the `authenticate` method of each, one-by-one from top to bottom with the credentials provided, until one accepts and returns a user. Upon getting a user the backend attr is set accordingly and the user is returned.
The authenticate method for the google-plus backend

See backends/base.py. All that happens here is that we check the kwargs backend key matches "google-plus" and if not we return None (which would cause django authenticate to continue its search for a matching backend for these creds). For us google-plus backend matches and we grab the pipeline (this just involves grabbing the list of function path strings from the SOCIAL_AUTH_PIPELINE of settings.py), set the user as not new by default, then if pipeline_index kwarg is present (we've already ran some of the pipeline are up to a given index in the list), we truncate the list from that point, before calling the method pipeline with the remaining list (for us on the first pass the index is non-existant so zero assumed as starting point).

##self.pipeline##

This just runs the pipeline, checking afterwards that the output of this bit of the pipeline is a dict. NB if it's not a dict the output is simply returned to the user, which is useful to know, since combined with the partial decorator that we'll meet later it means that we can effectively pause the pipeline while we return a HttpResponse, like form or some such, to the user for more input for example at some stage of the pipeline (this could be used to gather extra data from the user during registration for example)
If the pipeline just returned a dict then the user is grabbed from the dict, the attrs social_user and is_new are set accordingly, and the user is returned.
After the pipeline has ran the flow continues in actions.py do_complete, and involves checking the final user obtained is of the correct type specified by the user in the settings.py, USER_MODEL. We also pop the redirect_value from the session that was set earlier, under the session key specified by the redirect_name variable.
If authenticated redirect to the post flow url, else try to login using the login function provided (remember from apps/django_app/default/views.py that we passed the _do_login function (apps/django_app/views.py) to do_complete for this purpose, which just wraps around django login. That essentially finishes the flow.

##The pipeline##

The power of psa comes from the fact it uses a pipeline and by virtue of this the sign-in flow can be highly customized. Here I do a brief run down of the default pipeline:

	SOCIAL_AUTH_PIPELINE = (
        'social.pipeline.social_auth.social_details',
        'social.pipeline.social_auth.social_uid',
        'social.pipeline.social_auth.auth_allowed',
        'social.pipeline.social_auth.social_user',
        'social.pipeline.user.get_username',
        'social.pipeline.user.create_user',
        'social.pipeline.social_auth.associate_user',
        'social.pipeline.social_auth.load_extra_data',
        'social.pipeline.user.user_details',
 	)

##auth_social_details##

See pipeline/social_auth.py. Usually each pipeline function will return a dict, whose content will be added to the "out" dict, the combined dicts of the all the pipelines so far. The social details function is no exception, and it returns

 	{'details': backend.get_user_details(response)}

For `google-plus`, this get user details func is implemented in backends/google.py in the BaseGoogleAuth class. All it relly does is parse the response for keys like 'email', 'username', 'fullname', 'first_name', etc...

##auth_social_uid##

For g+ this function is implemented in backends/google.py in the BaseGoogleAuth class, if the user has set USE_UNIQUE_ID in settings.py, then the id from the response is used (for g+ this is known as the "sub id"), else the "email" that was just added to the 'detail' key by the previous pipeline function is used as the user's id.

##auth_allowed##

Calls backend.auth_allowed(response, details) raising an exception if the answer is False.
As you can see in backends.base.py this allows the psa user to use a whitelist of emails/domains, allowing only those emails/domains on whitelist to sign up. By default there is no whitelist and anyone can sign up...

##social_user##

psa uses the UserSocialAuth model (apps/django_app/default/models.py), which is Foreign Key'd to the user model, and stores certain extra info related to social authentication of the user. For example the provider, e.g. 'google-plus', the uid, which must be unique together with the provider. Methods for doing various things like create_user (follow the DjangoMixin hirearchy back), and finally via storage/base.py UserMixin storage of the access and refresh tokens, methods to do a refresh of the token etc...
The social user pipeline function, tries to get this UserSocialAuth object and set it to social. If it exists, we check the user it is associated to matches our user, and we add it the dictionary under the key 'social'.

##get_username##

Creates username for user if it doesn't exist based on settings

##create_user##

If user already present just return {'is_new': False}. Otherwise find out which fields a user should have (things like username, email) and as long as some fields exist pass them to strategy.create_user, returning is_new as True since we created a new user and returning this in the dict with the new user.
The strategies create user method is found in strategies/base.py and is just a wrapper for storage.user.create_user, which ultimately comes from apps/django_app/default/models.py DjangoStorage, which inherits from the DjangoUserMixin which has the create user method implemented. It just calls whatever create user method your user model itself defines.

##associate user##

If the user exists but the social auth user does not exist, the first task is to create the UserSocialAuth object to be linked with this user. Remember backend.strategy.storage is the DjangoStorage model of apps/django_app/default/models.py and the user attribute refers to the UserSocialAuth class. The UserSocialAuth class, inherits from the DjangoUserMixin (see storage/django_orm.py) the create_social_auth class method (so cls in this method refers to UserSocialAuth), so ultimately all we really do is call something tha translates to UserSocialAuth.objects.create..., to create a new social auth user. If no exceptions raised we return:

	{'social': social,
  	'user': social.user,
  	'new_association': True}

which will be appended to the out dictionary (notice this is a new association). The purpose of the UserSocialAuth model is to storage things like access tokens and other credentials.

##load extra data##

This function does what the name suggests, and there is not much to discuss. For google-plus the function is defined in backends/oauth.py and just adds the access token to the data, plus if user has set EXTRA_DATA this is also grabbed and added.

##user details##

This is also pretty straightfoward. For each name and value in the details dict we get the current attribute of the user under the 'name' key. If there is no current value and this name attribute is not disabled from updating (i.e. not in the SOCIAL_AUTH_PROTECTED_FIELDS setting list), then we update the attribute to the new value, making a note of the change under the "changed" bool of the user.

##Extra: Partial pipelines##

	def partial(func):
	    @wraps(func)
	    def wrapper(strategy, pipeline_index, *args, **kwargs):
	        out = func(strategy=strategy, pipeline_index=pipeline_index,
	                    *args, **kwargs) or {}
	        if not isinstance(out, dict):
	            values = strategy.partial_to_session(pipeline_index, *args,
	                                                 **kwargs)
	            strategy.session_set('partial_pipeline', values)
	        return out
    	return wrapper

The partial decorator is a simple decorator. Instead of just running a function in the pipeline, wrapping the function with the partial decorator first calls the function as usual, then decides what to do based on the response. If your function returns a dictionary then its output dict is returned like any regular pipeline and the pipeline trundles on just like as if you hadn't bothered using the decorator at all, but if you function returned something other than a dict (say for e.g. a HttpResponse like a form to collect more user data) then the pipeline up to this point is stored in the session temporarily while the response is returned to the user. The kwargs etc are cleaned and returned as a dict, stored as values, including the pipeline index as 'next', and this is then stored in the session.
Remember in actions.py do complete I deferred discussion of the

    partial = partial_pipeline_data(backend, user, *args, **kwargs)
    if partial:
    	xargs, xkwargs = partial
    	user = backend.continue_pipeline(*xargs, **xkwargs)

logic. Now when partial_pipeline_data (implemented in utils.py) is called, we find we do have a partial_pipeline key set in the session, we call partial_from_session to get all the stuff we stored in the session for the pipeline that had ran up to this point, such as the user, social, kwargs etc, and importantly next which will be the same pipeline index as it was before (we didn't increment it). This means partial does exist and we run backend.continue_pipeline(*xargs, **xkwargs) , which (backends/base.py) just wraps around the backend authenticate method, which for google as we saw earlier is implemented also in backends/base.py and involves running the pipeline at the appropriate pipeline index.
Ultimately all this means is that we have a way to pause the pipeline whilst we do something like gather user data. The pipeline up to that point is kept in the session, and the current pipeline function runs as many times as necessary until the response returned is a dict (i.e. you can keep returning something like a form, or a form with errors as many times as you need, and on success you return a dict to make the pipeline continue where it left off).