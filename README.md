# Windows-firewall-self-help-add-white-list
将脚本放入C:\Users\用户名\.qqbot-tmp\plugins

qqbot.py修改
	
	adminqq填写管理员的qq号
	ifqq填写允许自助添加ip的qq号
	
	
	默认防火墙的规则名为allow_TCP,位于158与173行
	可统一为变量控制名称
	
	
	管理员权限的命令
	@qqbot机器人 刷新所有
	@qqbot机器人 刷新好友
	@qqbot机器人 刷新讨论组
	@qqbot机器人 刷新组
	
	普通用户权限
	@qqbot机器人 添加OAIP *.*.*.*
	
	机器人的qq名称要为 qqbot机器人
	好友名称必须备注为qq号
	
	仅在讨论组测试没问题
	
	基于python2.7 qqbot2.3
	pip install qqbot==2.3
	
	v2.3.conf修改
	# 自动登录的 QQ 号
	        
	"qq" : "",
	        
	        
	# 接收二维码图片的邮箱账号
	        
	"mailAccount" : "",
	        
	        
	# 该邮箱的 IMAP/SMTP 服务授权码
	        
	"mailAuthCode" : "",
  
  
