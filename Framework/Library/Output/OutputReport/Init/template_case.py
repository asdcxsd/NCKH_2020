template_head = '''
<!DOCTYPE html>
<html>
<head lang="en">
    <meta charset="UTF-8">
    
</head>
<body>
<div style="text-align: center; font-weight: bold; ">
 <br><br><br><br><br><br><div style="font-size: 200%;">BÁO CÁO </div><br>
 Dò quét thông tin lỗ hổng bảo mật hệ thông<br><br>
{}
<br> 

</div>
'''
mark_I = '''
<h1 style="page-break-before : always; ">I Thông tin về  dò quét</h1>
'''
mark_1= '''
<h2>1.1 Thông tin tiến trình dò quét</h2>
'''
mark_2='''
<h2>1.2 Thông tin đối tượng dò quét</h2>
'''

mark_II='''
<h1 style="page-break-before : always;">II  Thu thập, dò quét thông tin</h1>
'''


mark_III='''
<h1 style="page-break-before : always;">III  Thông tin lỗ hổng bảo mật</h1>
'''

mark_IV='''
<h1 style="page-break-before : always;">IV  Lịch sử  khai thác lỗ hổng</h1>
'''

template_table = '''
<h4>{}</h4>
{} 
'''
template_tail = '''
</body>
</html>
'''
