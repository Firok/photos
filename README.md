# Photos project 
API to post a photo, save, edit, delete, list
 
 ## Setting up the development environment
see the requirements.txt and test_requirements.txt files

### Cloning the repository
```
cd /path/to/projects
git clone git@github.com:Firok/photos.git
cd ./photos
```

### Running the projects
```
docker-compose up
```

### Running test
```
docker exec -it photos_app pytest
```

### Endpoints
```
Now you can test the API swagger documentation at `https://firok-photos.herokuapp.com/api/docs/`:
```

### API to get access admin page
```
https://firok-photos.herokuapp.com/admin/

username: admin
password: admin@123

```


### API to get access token
```
https://firok-photos.herokuapp.com/api/token/
username: admin
password: admin@123

payload request
```
{
  "username": "admin",
  "password": "admin@123"
}
```

payload response
```
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTU5NjU2Njc1NiwianRpIjoiOWIxZGVhNTAxNGQ4NGNkMWFhODcxZTU0ZDE5MGM5MmUiLCJ1c2VyX2lkIjoyfQ.A7ZrY_VXn4cnRcCiyVUcw_ciMSYe6AgHATaAAWYqAnM",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTk2NDgwNjU2LCJqdGkiOiJiMGE2MTUzM2UxYTc0YWNmYTI2NGI4ZDc0MmE0ZTdkZCIsInVzZXJfaWQiOjJ9.aodTsmOzrx7R9J1OC7aK-nBKa708XCO1RC_21-uttJY"
}
```

```

### API to get all photos, drafts photos, photos by user
``` 
List all photos
`https://firok-photos.herokuapp.com/api/photos/`

Draft photos
`https://firok-photos.herokuapp.com/api/photos/?published=false`

Published photos
`https://firok-photos.herokuapp.com/api/photos/?published=true`

Filter by user
`https://firok-photos.herokuapp.com/api/photos/?user=1`

List ascending order by publish date
`https://firok-photos.herokuapp.com/api/photos/?ordering=published`

List descending order by publish date
`https://firok-photos.herokuapp.com/api/photos/?ordering=-published`
```

### API to upload photo
```
Method: POST
`https://firok-photos.herokuapp.com/api/photos/`
```


### API to get photo
```
Method: POST
`https://firok-photos.herokuapp.com/api/photos/{id}/
`
```

### API to edit photo
```
Method: PUT OR PATCH
`https://firok-photos.herokuapp.com/api/photos/{id}/
`
```

### API to delete photo
```
Method: DELETE
`https://firok-photos.herokuapp.com/api/photos/{id}/
`
```

### API to publish photo
```
Method: POST
`https://firok-photos.herokuapp.com/api/photos/{id}/publish/
`
```

### API to edit photos in batch
```
Method: PUT
`https://firok-photos.herokuapp.com/api/photos/batch_edit/
`
Payload Request
```
{
  "id": 0,
  "caption": "string"
}
```
```

### API to publish photos in batch
```
Method: POST
`https://firok-photos.herokuapp.com/api/photos/batch_publish/
`
Payload Request
```
{
  "ids": [
    1, 2
  ]
}
```
```

### API to delete photos in batch
```
Method: POST
`https://firok-photos.herokuapp.com/api/photos/batch_delete/
`
Payload Request
```
{
  "ids": [
    1, 2
  ]
}
```
```