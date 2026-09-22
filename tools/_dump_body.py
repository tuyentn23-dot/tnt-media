s=open('os_app/ui/index.html',encoding='utf-8',errors='replace').read()
# in tu sau </style> den <script>
i=s.find('</style>')
j=s.find('<script')
print('--- BODY ---')
print(s[i:j].encode('ascii','replace').decode('ascii'))
