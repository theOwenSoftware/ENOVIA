{
    "success": true,
    "statusCode": 200,
    "csrf": {
        "name": "ENO_CSRF_TOKEN",
        "value": "5U6Z-V3JP-QSAY-VM0Y-2I7W-5ZA9-P3RO-V2QB"
    },
    "items": 1,
    "data": [
        {
            "id": "296466B000002408678F603100000B16",   # un-changable
            "type": "Project Space", # un-changable
            "identifier": "296466B000002408678F603100000B16", # un-changable
            "source": "https://3de24xplm.com.tw:443/3dspace", # un-changable
            "relativePath": "/resources/v1/modeler/projects/296466B000002408678F603100000B16",
            "cestamp": "296466B00000240867909A0700000CB2", # self-change
            "dataelements": {
                "title": "fronted_test1",  # changable
                "name": "fronted_test1",   # changable(??)
                "revision": "1101737449521403", # un-changable
                "description": "owen test_put555",  # changable
                "state": "Create", # ????
                "originated": "2025-01-21T08:52:01.000Z",  # un-changable
                "modified": "2025-01-22T07:11:03.000Z", # present -time (?)
                "policy": "Project Space",  # un-changable
                "modifyAccess": "TRUE",  # un-changable
                "deleteAccess": "TRUE",  # un-changable
                "project": "DEMO_CS",  # un-changable
                "estimatedStartDate": "2025-01-21T08:00:00.000",  # un-changable
                "estimatedFinishDate": "2025-01-21T08:00:00.000",  # un-changable
                "dueDate": "2025-01-21T08:00:00.000",
                "actualStartDate": "",
                "actualFinishDate": "",
                "percentComplete": "0.0",
                "percentCompleteBasedOn": "Duration",
                "lagCalendar": "Successor Task Calendar",
                "estimatedDurationInputValue": "0.0",
                "estimatedDurationInputUnit": "d",
                "estimatedDuration": "0.0",
                "actualDuration": "0.0",
                "constraintDate": "2025-01-21T08:00:00.000",
                "defaultConstraintType": "As Soon As Possible",
                "scheduleFrom": "Project Start Date",
                "scheduleBasedOn": "Estimated",
                "projectVisibility": "Members",
                "notes": "",
                "typeicon": "https://3de24xplm.com.tw/3dspace/snresources/images/icons/small/I_ProjectSpace.png",
                "objType": "Project Space",
                "kindOfProjectSpace": "TRUE",
                "kindOfExperiment": "FALSE",
                "kindOfProjectBaseline": "FALSE",
                "kindOfProjectConcept": "FALSE",
                "kindOfProjectTemplate": "FALSE"
            },
            "relateddata": {
                "dpmParent": [],
                "subTypesInfo": [
                    {
                        "dataelements": {
                            "ProjectSpace": "ProjectSpace",
                            "ProjectConcept": "ProjectConcept",
                            "Experiment": "Experiment",
                            "ProjectSnapshot": "ProjectSpace",
                            "ProjectBaseline": "ProjectBaseline",
                            "Gate": "Gate",
                            "Milestone": "Milestone",
                            "Phase": "Phase",
                            "Task": "Task",
                            "PQPTask": "Task",
                            "VV_Test_Execution": "Task"
                        },
                        "children": []
                    }
                ],
                "subTypesAndPolicies": [
                    {
                        "dataelements": {
                            "Task": "[Project Task]#[Project Task]",
                            "Gate": "[Project Review]#[Project Review]",
                            "Milestone": "[Project Review]#[Project Review]",
                            "Phase": "[Project Task]#[Project Task]",
                            "AllTypes": "[Task, Gate, Milestone, Phase]",
                            "gateMilestoneTypes": "[Gate, Milestone]",
                            "InvalidChars": "\\\" # $ @ % * , ? \\\\ < > [ ] | : ; '",
                            "schedule": "Auto"
                        },
                        "children": []
                    }
                ],
                "performRollup": [
                    {
                        "id": "296466B000002408678F603100000B16",
                        "children": []
                    }
                ]
            },
            "children": []
        }
    ],
    "definitions": []
}



    {"data": [
        {
            "id": "296466B000002408678F603100000B16",
            "dataelements": {
                "title": "fronted_test_555555",
                "name": "fronted_test_555555",
                "description": "owen test_put_detail",
                "state": "Assign",
                "project": "DEMO_CS",
                "percentComplete": "0.0",
            },

        }
    ]
    }