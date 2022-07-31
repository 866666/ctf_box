选项:
  -h, --help            显示此帮助消息并退出

  Mandatory:
    -u URL, --url=URL   URL目标
    
    -L URLLIST, --url-list=URLLIST
                        URL列表目标
                        
    -e EXTENSIONS, --extensions=EXTENSIONS
                        以逗号分隔的扩展列表（示例：php、asp）
                        
    -E, --extensions-list
                        使用公共扩展的预定义列表

  Dictionary Settings:
    -w WORDLIST, --wordlist=WORDLIST
                        自定义单词表（用逗号分隔）
    -l, --lowercase
    -f, --force-extensions
                        强制扩展每个单词表条目（如DirBuster）

  常规设置:
    -s DELAY, --delay=DELAY
                        请求之间的延迟（浮点数）
                        
    -r, --recursive     递归暴力
    
    -R RECURSIVE_LEVEL_MAX, --recursive-level-max=RECURSIVE_LEVEL_MAX
                        最大递归级别（子目录）（默认值：1[仅限根目录+1目录]）
                        
    --suppress-empty, --suppress-empty
    --scan-subdir=SCANSUBDIRS, --scan-subdirs=SCANSUBDIRS
                        扫描给定-u |--url的子目录（分开逗号）
                        
    --exclude-subdir=EXCLUDESUBDIRS, --exclude-subdirs=EXCLUDESUBDIRS
                        在递归过程中排除下列子目录扫描（用逗号分隔）
                        
    -t THREADSCOUNT, --threads=THREADSCOUNT
                        线程数
                        
    -x EXCLUDESTATUSCODES, --exclude-status=EXCLUDESTATUSCODES
                        排除状态代码，用逗号分隔（例如：301，500个）
                        
    --exclude-texts=EXCLUDETEXTS
                        用逗号分隔的文本排除响应(示例: "Not found", "Error")
                        
    --exclude-regexps=EXCLUDEREGEXPS
                        按regexp排除响应，用逗号分隔(示例： "Not foun[a-z]{1}", "^Error$")
                        
    -c COOKIE, --cookie=COOKIE
    
    --ua=USERAGENT, --user-agent=USERAGENT 
   						用户代理
   						
    -F, --follow-redirects 
    					--遵循重定向
    					
    -H HEADERS, --header=HEADERS 页眉，--页眉=页眉
                        要添加的标题 (example: --header "Referer:
                        example.com" --header "User-Agent: IE"
                        
    --random-agents, --random-user-agents 
    					随机代理，--随机用户代理

  连接设置:
    --timeout=TIMEOUT   连接超时
    
    --ip=IP             将名称解析为IP地址
    
    --proxy=HTTPPROXY, --http-proxy=HTTPPROXY
                        Http代理 (example: localhost:8080
                        
    --http-method=HTTPMETHOD
                        要使用的方法，默认值：GET，也可能是：HEAD；POST
                        
    --max-retries=MAXRETRIES
    					最大重试次数
    					
    -b, --request-by-hostname
                        默认情况下，dirsearch将通过IP请求速度。
						这将强制按主机名请求

 报告:
    --simple-report=SIMPLEOUTPUTFILE 简单输出文件
                        只找到路径
                        
    --plain-text-report=PLAINTEXTOUTPUTFILE 纯文本输出文件
                        找到带有状态代码的路径
                        
    --json-report=JSONOUTPUTFILE JSON输出文件
