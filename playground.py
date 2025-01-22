# 請求 A 的參數
params_a = {
    "identifier": username,
    "service": f"{url_3dspace}/resources/v1/modeler/tasks",
}

headers_a = {
    "Accept": "application/json",
    "DS-Service-Name": DSServiceName,
    "DS-Service-Secret": DSServiceSecret,
}

try:
    response_a_1 = session.get(
        f"{url_3dpassport}/api/v2/batch/ticket",
        params=params_a,
        headers=headers_a,
        verify=cert,  # 在測試環境下禁用 SSL 驗證
    )
    if response_a_1.status_code == 200:
        data = response_a_1.json()

        x3dsreauthurl = data["x3ds_reauth_url"]
        print("Request A 成功，Cookie 已儲存至 Session")

        print("返回內容：", response_a_1.json())
    else:
        print("Request A 失敗，狀態碼：", response_a_1.status_code)
        print("返回內容：", response_a_1.text)
except requests.exceptions.RequestException as e:
    print("Request A 發生錯誤：", e)

# 檢查 Session 中的 Cookie
print("Session Cookies:", session.cookies)



# Request_2
try:
    # 發送 GET 請求
    response = session.get(x3dsreauthurl,    
    headers=headers_a, 
    verify=cert)

    # 檢查請求是否成功
    if response.status_code == 200:
        data = response.json()
        x3ds_service_redirect_url = data["x3ds_service_redirect_url"]
        # print("取得x3ds_service_redirect_url：", x3ds_service_redirect_url)
        print("Request_2 ：成功")

    else:
        print("請求失敗，狀態碼：", response.status_code)
        print("錯誤回應內容：", response.text)
except requests.exceptions.SSLError as e:
    print("SSL 憑證錯誤：", e)
except requests.exceptions.RequestException as e:
    print("請求錯誤：", e)

# 請求 B：使用請求 A 的 Cookie
try:
    response_b = session.post(
        "https://3de24xplm.com.tw/3dspace/resources/v1/modeler/projects",
        headers=headers_b,
        params=params_b,
        json=request_body_b,
        verify=cert, 
    )
    # print("Session Cookies After POST:", session.cookies)
    if response_b.status_code == 200:
        print("Request B 成功")
        print("返回內容：", response_b.json())
    else:
        print("Request B 失敗，狀態碼：", response_b.status_code)
        print("返回內容：", response_b.text)
except requests.exceptions.RequestException as e:
    print("Request B 發生錯誤：", e)
    print("返回內容：", response_b.text)







import requests
import json

url_3dpassport = "https://3de24xplm.com.tw/3dpassport"
url_3dspace ="https://3de24xplm.com.tw/3dspace"
username = "nikki"
DSServiceName = "DemoService"
# print("DSServiceName :",DSServiceName)
DSServiceSecret = "0bc65bcb-56df-45e9-b998-ab4f02c48eb8"
# print("DSServiceSecret :",DSServiceSecret)

x3dsreauthurl = ""
x3ds_service_redirect_url = ""

# Routes Test
ServiceRoutes = "resources/v1/modeler/dsrt/routes/search" # (get)取得所有Route內容
ServiceRoutes_ID = "resources/v1/modeler/dsrt/routes/291727550000070065E9629B00000880"  # (get)透過ID，取得特定Route內容
ServiceRoutes_create = "resources/v1/modeler/dsrt/routes" # (post)
ServiceRoutes_delete = "resources/v1/modeler/dsrt/routes/delete" # (post)
ServiceRoutes_templates = "resources/v1/modeler/dsrt/routetemplates/search" # (get)

# Projest Test
ServiceProject = "resources/v1/modeler/projects"  # (get)
ServiceProject_ID = "resources/v1/modeler/projects/296466B0000025EC6784728500000172"  # (get)
ServiceProject_create = "resources/v1/modeler/projects"  # (post)

# Task Test
ServiceTasks = "resources/v1/modeler/tasks"

params = {
    "identifier": username,
    # "service": f"{url_3dspace}/{ServiceTasks}",
    # "service": f"{url_3dspace}/{ServiceProject}",
    # "service": f"{url_3dspace}/{ServiceProject_ID}",
    "service": f"{url_3dspace}/{ServiceProject_create}",
    # "Content-Type":"application/x-www-form-urlencoded;charset=UTF-8"
    # "service": f"{url_3dspace}/{ServiceRoutes}",
    # "service": f"{url_3dspace}/{ServiceRoutes_templates}",
    # "service": f"{url_3dspace}/{ServiceRoutes_ID}",
    # "service": f"{url_3dspace}/{ServiceRoutes_delete}",
}

headers = {
    "Accept": "application/json",         
    "DS-Service-Name": DSServiceName,
    "DS-Service-Secret": DSServiceSecret    

}



request_body = {
    "data": [
        {
            "type": "Project",                  # 專案類型
            "dataelements": {
                "title": "New Project Title",   # 替換為你的專案標題
                "description": "Project Description",  # 替換為描述
                "projectVisibility": "Public", # 專案可見性（Public 或 Members）
                "estimatedStartDate": "2025-01-15",  # 預計開始日期
                "estimatedFinishDate": "2025-06-30"  # 預計結束日期
            }
        }
    ]
}

cert = "3de24xplm.crt"
# Request_1
try:
    # 發送 GET 請求
    response = requests.get(f"{url_3dpassport}/api/v2/batch/ticket", params=params, headers=headers, verify=cert)
    # response = requests.get(f"{url_3dpassport}/api/v2/batch/ticket", params=params, headers=headers, json=request_body, verify=cert)

    response = requests.post(
        f"{url_3dpassport}/api/v2/batch/ticket", 
        params=params, 
        headers=headers, 
        json=request_body, 
        verify=cert
    )

    # 檢查請求是否成功
    if response.status_code == 200:
        data = response.json()
        x3dsreauthurl = data["x3ds_reauth_url"]
        # print("取得x3ds_reauth_url ：", x3dsreauthurl)
        print("Request_1 ：成功")
    else:
        print("請求失敗，狀態碼：", response.status_code)
        print("錯誤回應內容：", response.text)
except requests.exceptions.SSLError as e:
    print("SSL 憑證錯誤：", e)
except requests.exceptions.RequestException as e:
    print("請求錯誤：", e)


# Request_2
try:
    # 發送 GET 請求
    response = requests.get(x3dsreauthurl, headers=headers, json=request_body,verify=False)

    # 檢查請求是否成功
    if response.status_code == 200:
        data = response.json()
        x3ds_service_redirect_url = data["x3ds_service_redirect_url"]
        # print("取得x3ds_service_redirect_url：", x3ds_service_redirect_url)
        print("Request_2 ：成功")

    else:
        print("請求失敗，狀態碼：", response.status_code)
        print("錯誤回應內容：", response.text)
except requests.exceptions.SSLError as e:
    print("SSL 憑證錯誤：", e)
except requests.exceptions.RequestException as e:
    print("請求錯誤：", e)

# Request_3
try:
    # 發送 GET 請求
    response = requests.get(x3ds_service_redirect_url, headers=headers, json=request_body,verify=False)

    # 檢查請求是否成功
    if response.status_code == 200:
        data = response.json()
        json_data = json.dumps(data, indent=None, ensure_ascii=False)  # 格式化為 JSON 字串
        print("Request_3 ：成功")
        print("取得的資料：", json_data)
    else:
        print("請求失敗，狀態碼：", response.status_code)
        print("錯誤回應內容：", response.text)
except requests.exceptions.SSLError as e:
    print("SSL 憑證錯誤：", e)
except requests.exceptions.RequestException as e:
    print("請求錯誤：", e)

{
  "data": [
    {
      "id": "000000800000000C0000000000000000",
      "type": "string",
      "identifier": "000000800000000C0000000000000000",
      "source": "https://3dspace.mydomain:443/3dspace",
      "relativePath": "/resources/v1/modeler/samples/000000800000000C0000000000000000",
      "cestamp": "857FEB80000045FC5994CC0A00000012",
      "dataelements": {
        "description": "string",
        "state": "string",
        "estimatedStartDate": "string",
        "estimatedFinishDate": "string",
        "actualStartDate": "string",
        "actualFinishDate": "string",
        "nlsType": "string",
        "color": "string",
        "pattern": "string",
        "ganttConfig": "string",
        "kindofBaseline": "string",
        "kindofExperiment": "string",
        "kindofTemplate": "string",
        "kindofConcept": "string",
        "routeId": "string",
        "columns": "string",
        "estimatedDurationInputValue": "string",
        "estimatedDuration": "string",
        "forecastDuration": "string",
        "forecastStartDate": "string",
        "forecastFinishDate": "string",
        "constraintType": "string",
        "constraintDate": "string",
        "defaultConstraintType": "string",
        "scheduleFrom": "string",
        "scheduleBasedOn": "string",
        "projectVisibility": "string",
        "currency": "string",
        "notes": "string",
        "status": "string"
      },
      "relelements": {
        "sequenceOrder": "string"
      },
      "relateddata": {
        "ownerInfo": [
          {
            "id": "000000800000000C0000000000000000",
            "type": "string",
            "identifier": "000000800000000C0000000000000000",
            "source": "https://3dspace.mydomain:443/3dspace",
            "relativePath": "/resources/v1/modeler/samples/000000800000000C0000000000000000",
            "cestamp": "857FEB80000045FC5994CC0A00000012",
            "dataelements": {},
            "relateddata": {
              "calendar": [
                {
                  "id": "000000800000000C0000000000000000",
                  "type": "string",
                  "identifier": "000000800000000C0000000000000000",
                  "source": "https://3dspace.mydomain:443/3dspace",
                  "relativePath": "/resources/v1/modeler/samples/000000800000000C0000000000000000",
                  "cestamp": "857FEB80000045FC5994CC0A00000012",
                  "dataelements": {
                    "title": "string",
                    "default": "string"
                  }
                }
              ]
            }
          }
        ],
        "originatorInfo": [
          {
            "id": "000000800000000C0000000000000000",
            "type": "string",
            "identifier": "000000800000000C0000000000000000",
            "source": "https://3dspace.mydomain:443/3dspace",
            "relativePath": "/resources/v1/modeler/samples/000000800000000C0000000000000000",
            "cestamp": "857FEB80000045FC5994CC0A00000012",
            "dataelements": {},
            "relateddata": {
              "calendar": [
                {
                  "id": "000000800000000C0000000000000000",
                  "type": "string",
                  "identifier": "000000800000000C0000000000000000",
                  "source": "https://3dspace.mydomain:443/3dspace",
                  "relativePath": "/resources/v1/modeler/samples/000000800000000C0000000000000000",
                  "cestamp": "857FEB80000045FC5994CC0A00000012",
                  "dataelements": {
                    "title": "string",
                    "default": "string"
                  }
                }
              ]
            }
          }
        ],
        "tasks": [
          {
            "id": "000000800000000C0000000000000000",
            "type": "string",
            "identifier": "000000800000000C0000000000000000",
            "source": "https://3dspace.mydomain:443/3dspace",
            "relativePath": "/resources/v1/modeler/samples/000000800000000C0000000000000000",
            "cestamp": "857FEB80000045FC5994CC0A00000012",
            "dataelements": {
              "title": "\n",
              "description": "string",
              "state": "Create",
              "taskRequirement": "Optional",
              "notes": "string",
              "needsReview": "No",
              "percentComplete": "string",
              "estimatedStartDate": "string",
              "dueDate": "string",
              "estimatedDurationInputValue": "0.0",
              "estimatedDurationInputUnit": "0.0",
              "estimatedDuration": "0.0",
              "actualStartDate": "string",
              "actualFinishDate": "string",
              "actualDuration": "string",
              "forecastStartDate": "string",
              "forecastFinishDate": "string",
              "forecastDuration": "string",
              "constraintType": "",
              "constraintDate": "string",
              "scheduleFrom": "Project Start Date",
              "scheduleBasedOn": "Estimated",
              "projectVisibility": "Members",
              "routeTaskDueDate": "string",
              "routeTaskApprovalAction": "Approve",
              "routeTaskApprovalComments": "string",
              "routeTaskReviewerComments": "string",
              "freeFloat": "string",
              "totalFloat": "string",
              "isOverallCritical": "string",
              "nlsType": "string",
              "pattern": "string",
              "color": "string",
              "isSummaryTask": "string",
              "effortId": "string",
              "sourceId": "string",
              "taskProjectId": "string",
              "passiveSubtask": "string",
              "criticalTask": "FALSE",
              "Deviation": "string",
              "predictiveActualFinishDate": "string"
            },
            "relelements": {
              "sequenceOrder": "string"
            },
            "relateddata": {
              "predecessors": [
                {
                  "id": "000000800000000C0000000000000000",
                  "type": "string",
                  "identifier": "000000800000000C0000000000000000",
                  "source": "https://3dspace.mydomain:443/3dspace",
                  "relativePath": "/resources/v1/modeler/samples/000000800000000C0000000000000000",
                  "cestamp": "857FEB80000045FC5994CC0A00000012",
                  "dataelements": {
                    "title": "string"
                  },
                  "relelements": {
                    "lagTime": "0.0",
                    "dependencyType": "FS",
                    "lagTimeInputUnit": "0.0",
                    "lagTimeInputValue": "0.0",
                    "From": "string",
                    "predTaskSeqNumber": "string",
                    "To": "string",
                    "predProjectName": "string",
                    "predProjectId": "string"
                  }
                }
              ],
              "ownerInfo": [
                {
                  "id": "000000800000000C0000000000000000",
                  "type": "string",
                  "identifier": "000000800000000C0000000000000000",
                  "source": "https://3dspace.mydomain:443/3dspace",
                  "relativePath": "/resources/v1/modeler/samples/000000800000000C0000000000000000",
                  "cestamp": "857FEB80000045FC5994CC0A00000012",
                  "dataelements": {},
                  "relateddata": {
                    "calendar": [
                      {
                        "id": "000000800000000C0000000000000000",
                        "type": "string",
                        "identifier": "000000800000000C0000000000000000",
                        "source": "https://3dspace.mydomain:443/3dspace",
                        "relativePath": "/resources/v1/modeler/samples/000000800000000C0000000000000000",
                        "cestamp": "857FEB80000045FC5994CC0A00000012",
                        "dataelements": {
                          "title": "string",
                          "default": "string"
                        }
                      }
                    ]
                  }
                }
              ],
              "originatorInfo": [
                {
                  "id": "000000800000000C0000000000000000",
                  "type": "string",
                  "identifier": "000000800000000C0000000000000000",
                  "source": "https://3dspace.mydomain:443/3dspace",
                  "relativePath": "/resources/v1/modeler/samples/000000800000000C0000000000000000",
                  "cestamp": "857FEB80000045FC5994CC0A00000012",
                  "dataelements": {},
                  "relateddata": {
                    "calendar": [
                      {
                        "id": "000000800000000C0000000000000000",
                        "type": "string",
                        "identifier": "000000800000000C0000000000000000",
                        "source": "https://3dspace.mydomain:443/3dspace",
                        "relativePath": "/resources/v1/modeler/samples/000000800000000C0000000000000000",
                        "cestamp": "857FEB80000045FC5994CC0A00000012",
                        "dataelements": {
                          "title": "string",
                          "default": "string"
                        }
                      }
                    ]
                  }
                }
              ],
              "references": [
                {
                  "id": "000000800000000C0000000000000000",
                  "type": "string",
                  "identifier": "000000800000000C0000000000000000",
                  "source": "https://3dspace.mydomain:443/3dspace",
                  "relativePath": "/resources/v1/modeler/samples/000000800000000C0000000000000000",
                  "cestamp": "857FEB80000045FC5994CC0A00000012",
                  "dataelements": {
                    "description": "string",
                    "state": "string"
                  }
                }
              ],
              "deliverables": [
                {
                  "id": "000000800000000C0000000000000000",
                  "type": "string",
                  "identifier": "000000800000000C0000000000000000",
                  "source": "https://3dspace.mydomain:443/3dspace",
                  "relativePath": "/resources/v1/modeler/samples/000000800000000C0000000000000000",
                  "cestamp": "857FEB80000045FC5994CC0A00000012",
                  "dataelements": {
                    "name": "string",
                    "revision": "string",
                    "title": "\n",
                    "synopsis": "string",
                    "firstname": "Unknown",
                    "lastname": "Unknown",
                    "fullname": "Unknown",
                    "objectId": "string",
                    "policy": "string",
                    "stateNLS": "string",
                    "typeNLS": "string",
                    "collabSpace": "string",
                    "collabSpaceTitle": "string",
                    "organization": "string",
                    "organizationTitle": "string",
                    "ownerFullname": "string",
                    "hasfiles": [
                      "string"
                    ],
                    "fileExtension": [
                      "string"
                    ],
                    "linkURL": "string"
                  }
                }
              ],
              "route": [
                {
                  "id": "000000800000000C0000000000000000",
                  "type": "string",
                  "identifier": "000000800000000C0000000000000000",
                  "source": "https://3dspace.mydomain:443/3dspace",
                  "relativePath": "/resources/v1/modeler/samples/000000800000000C0000000000000000",
                  "cestamp": "857FEB80000045FC5994CC0A00000012",
                  "dataelements": {
                    "name": "string"
                  }
                }
              ],
              "scopes": [
                {
                  "id": "000000800000000C0000000000000000",
                  "type": "string",
                  "identifier": "000000800000000C0000000000000000",
                  "source": "https://3dspace.mydomain:443/3dspace",
                  "relativePath": "/resources/v1/modeler/samples/000000800000000C0000000000000000",
                  "cestamp": "857FEB80000045FC5994CC0A00000012",
                  "dataelements": {
                    "name": "string",
                    "revision": "string",
                    "title": "\n",
                    "synopsis": "string",
                    "firstname": "Unknown",
                    "lastname": "Unknown",
                    "fullname": "Unknown",
                    "objectId": "string",
                    "policy": "string",
                    "stateNLS": "string",
                    "typeNLS": "string",
                    "collabSpace": "string",
                    "collabSpaceTitle": "string",
                    "organization": "string",
                    "organizationTitle": "string",
                    "ownerFullname": "string",
                    "hasfiles": [
                      "string"
                    ],
                    "fileExtension": [
                      "string"
                    ]
                  }
                }
              ],
              "contents": [
                {
                  "id": "000000800000000C0000000000000000",
                  "type": "string",
                  "identifier": "000000800000000C0000000000000000",
                  "source": "https://3dspace.mydomain:443/3dspace",
                  "relativePath": "/resources/v1/modeler/samples/000000800000000C0000000000000000",
                  "cestamp": "857FEB80000045FC5994CC0A00000012",
                  "dataelements": {
                    "name": "string",
                    "revision": "string",
                    "title": "\n",
                    "synopsis": "string",
                    "firstname": "Unknown",
                    "lastname": "Unknown",
                    "fullname": "Unknown",
                    "objectId": "string",
                    "policy": "string",
                    "stateNLS": "string",
                    "typeNLS": "string",
                    "collabSpace": "string",
                    "collabSpaceTitle": "string",
                    "organization": "string",
                    "organizationTitle": "string",
                    "ownerFullname": "string",
                    "hasfiles": [
                      "string"
                    ],
                    "fileExtension": [
                      "string"
                    ]
                  }
                }
              ],
              "assignees": [
                {
                  "id": "000000800000000C0000000000000000",
                  "type": "string",
                  "identifier": "000000800000000C0000000000000000",
                  "source": "https://3dspace.mydomain:443/3dspace",
                  "relativePath": "/resources/v1/modeler/samples/000000800000000C0000000000000000",
                  "cestamp": "857FEB80000045FC5994CC0A00000012",
                  "dataelements": {},
                  "relateddata": {
                    "calendar": [
                      {
                        "id": "000000800000000C0000000000000000",
                        "type": "string",
                        "identifier": "000000800000000C0000000000000000",
                        "source": "https://3dspace.mydomain:443/3dspace",
                        "relativePath": "/resources/v1/modeler/samples/000000800000000C0000000000000000",
                        "cestamp": "857FEB80000045FC5994CC0A00000012",
                        "dataelements": {
                          "title": "string",
                          "default": "string"
                        }
                      }
                    ]
                  }
                }
              ],
              "calendar": [
                {
                  "id": "000000800000000C0000000000000000",
                  "type": "string",
                  "identifier": "000000800000000C0000000000000000",
                  "source": "https://3dspace.mydomain:443/3dspace",
                  "relativePath": "/resources/v1/modeler/samples/000000800000000C0000000000000000",
                  "cestamp": "857FEB80000045FC5994CC0A00000012",
                  "dataelements": {
                    "title": "string",
                    "default": "string"
                  }
                }
              ]
            }
          }
        ],
        "members": [
          {
            "id": "000000800000000C0000000000000000",
            "type": "string",
            "identifier": "000000800000000C0000000000000000",
            "source": "https://3dspace.mydomain:443/3dspace",
            "relativePath": "/resources/v1/modeler/samples/000000800000000C0000000000000000",
            "cestamp": "857FEB80000045FC5994CC0A00000012",
            "dataelements": {},
            "relelements": {},
            "relateddata": {
              "calendar": [
                {
                  "id": "000000800000000C0000000000000000",
                  "type": "string",
                  "identifier": "000000800000000C0000000000000000",
                  "source": "https://3dspace.mydomain:443/3dspace",
                  "relativePath": "/resources/v1/modeler/samples/000000800000000C0000000000000000",
                  "cestamp": "857FEB80000045FC5994CC0A00000012",
                  "dataelements": {
                    "title": "string",
                    "default": "string"
                  }
                }
              ]
            }
          }
        ],
        "risks": [
          {
            "id": "000000800000000C0000000000000000",
            "type": "string",
            "identifier": "000000800000000C0000000000000000",
            "source": "https://3dspace.mydomain:443/3dspace",
            "relativePath": "/resources/v1/modeler/samples/000000800000000C0000000000000000",
            "cestamp": "857FEB80000045FC5994CC0A00000012",
            "dataelements": {
              "description": "string",
              "state": "string",
              "estimatedStartDate": "string",
              "estimatedFinishDate": "string",
              "riskType": "Cost",
              "riskVisibility": "Public",
              "riskImpact": "1",
              "riskProbability": "1",
              "riskResolution": "string",
              "riskAbatement": "string",
              "measureOfSuccess": "string",
              "riskCategory": ""
            },
            "relateddata": {
              "assignees": [
                {
                  "id": "000000800000000C0000000000000000",
                  "type": "string",
                  "identifier": "000000800000000C0000000000000000",
                  "source": "https://3dspace.mydomain:443/3dspace",
                  "relativePath": "/resources/v1/modeler/samples/000000800000000C0000000000000000",
                  "cestamp": "857FEB80000045FC5994CC0A00000012",
                  "dataelements": {},
                  "relateddata": {
                    "calendar": [
                      {
                        "id": "000000800000000C0000000000000000",
                        "type": "string",
                        "identifier": "000000800000000C0000000000000000",
                        "source": "https://3dspace.mydomain:443/3dspace",
                        "relativePath": "/resources/v1/modeler/samples/000000800000000C0000000000000000",
                        "cestamp": "857FEB80000045FC5994CC0A00000012",
                        "dataelements": {
                          "title": "string",
                          "default": "string"
                        }
                      }
                    ]
                  }
                }
              ],
              "ownerInfo": [
                {
                  "id": "000000800000000C0000000000000000",
                  "type": "string",
                  "identifier": "000000800000000C0000000000000000",
                  "source": "https://3dspace.mydomain:443/3dspace",
                  "relativePath": "/resources/v1/modeler/samples/000000800000000C0000000000000000",
                  "cestamp": "857FEB80000045FC5994CC0A00000012",
                  "dataelements": {},
                  "relateddata": {
                    "calendar": [
                      {
                        "id": "000000800000000C0000000000000000",
                        "type": "string",
                        "identifier": "000000800000000C0000000000000000",
                        "source": "https://3dspace.mydomain:443/3dspace",
                        "relativePath": "/resources/v1/modeler/samples/000000800000000C0000000000000000",
                        "cestamp": "857FEB80000045FC5994CC0A00000012",
                        "dataelements": {
                          "title": "string",
                          "default": "string"
                        }
                      }
                    ]
                  }
                }
              ],
              "rpn": [
                {
                  "id": "000000800000000C0000000000000000",
                  "type": "string",
                  "identifier": "000000800000000C0000000000000000",
                  "source": "https://3dspace.mydomain:443/3dspace",
                  "relativePath": "/resources/v1/modeler/samples/000000800000000C0000000000000000",
                  "cestamp": "857FEB80000045FC5994CC0A00000012",
                  "dataelements": {}
                }
              ]
            }
          }
        ],
        "subTypesInfo": [
          {
            "id": "000000800000000C0000000000000000",
            "type": "string",
            "identifier": "000000800000000C0000000000000000",
            "source": "https://3dspace.mydomain:443/3dspace",
            "relativePath": "/resources/v1/modeler/samples/000000800000000C0000000000000000",
            "cestamp": "857FEB80000045FC5994CC0A00000012"
          }
        ],
        "issues": [
          {
            "id": "000000800000000C0000000000000000",
            "type": "string",
            "identifier": "000000800000000C0000000000000000",
            "source": "https://3dspace.mydomain:443/3dspace",
            "relativePath": "/resources/v1/modeler/samples/000000800000000C0000000000000000",
            "cestamp": "857FEB80000045FC5994CC0A00000012",
            "dataelements": {
              "description": "string",
              "state": "string",
              "estimatedFinishDate": "string",
              "problemType": "Not Determined",
              "priority": "Low",
              "priorityInternal": "Unassigned",
              "actionTaken": "string",
              "resolution": "string",
              "steps": "string"
            },
            "relateddata": {
              "assignees": [
                {
                  "id": "000000800000000C0000000000000000",
                  "type": "string",
                  "identifier": "000000800000000C0000000000000000",
                  "source": "https://3dspace.mydomain:443/3dspace",
                  "relativePath": "/resources/v1/modeler/samples/000000800000000C0000000000000000",
                  "cestamp": "857FEB80000045FC5994CC0A00000012",
                  "dataelements": {},
                  "relateddata": {
                    "calendar": [
                      {
                        "id": "000000800000000C0000000000000000",
                        "type": "string",
                        "identifier": "000000800000000C0000000000000000",
                        "source": "https://3dspace.mydomain:443/3dspace",
                        "relativePath": "/resources/v1/modeler/samples/000000800000000C0000000000000000",
                        "cestamp": "857FEB80000045FC5994CC0A00000012",
                        "dataelements": {
                          "title": "string",
                          "default": "string"
                        }
                      }
                    ]
                  }
                }
              ],
              "ownerInfo": [
                {
                  "id": "000000800000000C0000000000000000",
                  "type": "string",
                  "identifier": "000000800000000C0000000000000000",
                  "source": "https://3dspace.mydomain:443/3dspace",
                  "relativePath": "/resources/v1/modeler/samples/000000800000000C0000000000000000",
                  "cestamp": "857FEB80000045FC5994CC0A00000012",
                  "dataelements": {},
                  "relateddata": {
                    "calendar": [
                      {
                        "id": "000000800000000C0000000000000000",
                        "type": "string",
                        "identifier": "000000800000000C0000000000000000",
                        "source": "https://3dspace.mydomain:443/3dspace",
                        "relativePath": "/resources/v1/modeler/samples/000000800000000C0000000000000000",
                        "cestamp": "857FEB80000045FC5994CC0A00000012",
                        "dataelements": {
                          "title": "string",
                          "default": "string"
                        }
                      }
                    ]
                  }
                }
              ],
              "originatorInfo": [
                {
                  "id": "000000800000000C0000000000000000",
                  "type": "string",
                  "identifier": "000000800000000C0000000000000000",
                  "source": "https://3dspace.mydomain:443/3dspace",
                  "relativePath": "/resources/v1/modeler/samples/000000800000000C0000000000000000",
                  "cestamp": "857FEB80000045FC5994CC0A00000012",
                  "dataelements": {},
                  "relateddata": {
                    "calendar": [
                      {
                        "id": "000000800000000C0000000000000000",
                        "type": "string",
                        "identifier": "000000800000000C0000000000000000",
                        "source": "https://3dspace.mydomain:443/3dspace",
                        "relativePath": "/resources/v1/modeler/samples/000000800000000C0000000000000000",
                        "cestamp": "857FEB80000045FC5994CC0A00000012",
                        "dataelements": {
                          "title": "string",
                          "default": "string"
                        }
                      }
                    ]
                  }
                }
              ]
            }
          }
        ],
        "folders": [
          {
            "id": "000000800000000C0000000000000000",
            "type": "string",
            "identifier": "000000800000000C0000000000000000",
            "source": "https://3dspace.mydomain:443/3dspace",
            "relativePath": "/resources/v1/modeler/samples/000000800000000C0000000000000000",
            "cestamp": "857FEB80000045FC5994CC0A00000012",
            "dataelements": {
              "name": "string",
              "description": "string",
              "accessType": "Inherited",
              "folderClassification": "Shared",
              "title": "\n",
              "originated": "string",
              "modifyAccess": "string",
              "addAccess": "string",
              "removeAccess": "string",
              "deleteAccess": "string",
              "state": "Create",
              "project": "string",
              "organization": "string"
            },
            "relateddata": {
              "content": [
                {
                  "id": "000000800000000C0000000000000000",
                  "type": "string",
                  "identifier": "000000800000000C0000000000000000",
                  "source": "https://3dspace.mydomain:443/3dspace",
                  "relativePath": "/resources/v1/modeler/samples/000000800000000C0000000000000000",
                  "cestamp": "857FEB80000045FC5994CC0A00000012",
                  "dataelements": {
                    "name": "string",
                    "revision": "string",
                    "title": "\n",
                    "synopsis": "string",
                    "firstname": "Unknown",
                    "lastname": "Unknown",
                    "fullname": "Unknown",
                    "objectId": "string",
                    "policy": "string",
                    "stateNLS": "string",
                    "typeNLS": "string",
                    "collabSpace": "string",
                    "collabSpaceTitle": "string",
                    "organization": "string",
                    "organizationTitle": "string",
                    "ownerFullname": "string",
                    "hasfiles": [
                      "string"
                    ],
                    "fileExtension": [
                      "string"
                    ]
                  }
                }
              ],
              "sovaccess": [
                {
                  "id": "000000800000000C0000000000000000",
                  "type": "string",
                  "identifier": "000000800000000C0000000000000000",
                  "source": "https://3dspace.mydomain:443/3dspace",
                  "relativePath": "/resources/v1/modeler/samples/000000800000000C0000000000000000",
                  "cestamp": "857FEB80000045FC5994CC0A00000012",
                  "dataelements": {
                    "orgnization": "string",
                    "project": "string",
                    "person": "string",
                    "access": "string",
                    "comment": "string"
                  }
                }
              ]
            }
          }
        ],
        "calendar": [
          {
            "id": "000000800000000C0000000000000000",
            "type": "string",
            "identifier": "000000800000000C0000000000000000",
            "source": "https://3dspace.mydomain:443/3dspace",
            "relativePath": "/resources/v1/modeler/samples/000000800000000C0000000000000000",
            "cestamp": "857FEB80000045FC5994CC0A00000012",
            "dataelements": {
              "title": "string",
              "default": "string"
            }
          }
        ]
      }
    }
  ]
}