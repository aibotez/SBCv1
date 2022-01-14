"""filedown URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from django.conf import settings
from django.conf.urls. static import static
from . import view,view_bf,view_share,view_khd,view_zyh,view_baidu_net,view_tuozh

urlpatterns = [
    path('admin/', admin.site.urls),
    path('s', view.ct),
    path('bk', view.per_page),
    path('user_cz',view.user_cz),
    path('start/', view.ho),
    path('wenjcl/', view.wenjcl),
    path('dlzc/', view.dlzc),
    path('', view.shouye),
    path('wenjcl/del_fie/',view.del_fie),
 #   path('delcookies/', view.shouye),
    path('xhy_web_video_bf/',view.xhy_web_video_bf),

    path('myp/', view.my_image),

    # path('fehome/', view.fehome),
    path('netcz/', view.netcz),
    path('down_khd/',view.down_khd),
    path('down_khd/khd_down_act/',view.down_khd_act),



    path('check_romote_fes/',view_bf.check_romote_fes),
    path('check_user_bf/',view_bf.check_user_bf),
    re_path(r's/xiaz/(?P<id>[0.0.0.0-90.90.90.90]+)$', view.xiaz),
    path('share/', view_share.share_to),
    path('share_url/', view_share.share_re),
    path('share_url/bk/', view_share.back),
    path('share_url/share_fe_left_cz/', view_share.fe_left_cz),
    path('share_url/cz', view_share.share_fe_cz),
    path('share_url/share_fe_left_cz/cz/', view_share.share_fe_cz),
    path('share_url/share_fe_left_cz/bk/',view_share.back),
    path('share_url/share_fe_left_cz/wenjcl/',view_share.down),
    path('share_url/wenjcl/',view_share.down),


    path('khd_fe_re/',view_khd.khd_qq),
    path('khd_xz/',view_khd.khd_xz),
    path('khd_copy_pste/',view_khd.zhant),
    path('khd_del_fe/', view_khd.del_fe),
    path('khd_upfe/', view_khd.up_fes),
    path('khd_rename/',view_khd.rename),
    path('get_fe_info/',view_khd.get_fe_info),
    path('get_size/',view_khd.get_size),
    path('get_user_info/',view_khd.get_user_info),
    path('pdf_c_jpg/',view_khd.pdf_c_jpg),
    path('khd_yl/',view_khd.khd_yl),
    path('get_fe_info_judge/',view_khd.get_fe_info_judge),
    path('khd_version_judge/',view_khd.khd_version_judge),
    path('get_fe_size/',view_khd.get_fe_size),
    path('return_fie_chunk/',view_khd.return_fie_chunk),
    path('re_ip_list/',view_khd.re_ip_list),
    path('up_fie_chunk/',view_khd.up_fie_chunk),
    path('getmd5/',view_khd.getmd5),
    path('complexfie/',view_khd.complexfie),


    path('zyh/',view_zyh.se_zy),
    re_path(r'video_id/(?P<id>[00000-99999]+)$',view_zyh.chose_v),
    path('zyh_chose_page/',view_zyh.chose_page),
    path('zyh_chose_page/page_cz/',view_zyh.page_cz),
    re_path(r'video_bf_id/(?P<id>[00000-99999]+)$',view_zyh.bf_video),

    path('test/',view_zyh.test),
    path('test_se/',view_zyh.test_se),
    path('zyh_chose_page/video_id/zyh_down/',view_zyh.zyh_down),

    path('baidunet/',view_baidu_net.baidu_net),
    path('baidu_net_ss/',view_baidu_net.baidu_net_ss),


    path('gi/',view_tuozh.get_user_ip_home),
    path('gi/gii/', view_tuozh.get_ip),
    



]
