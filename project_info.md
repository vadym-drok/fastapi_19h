[Stop in ->](https://youtu.be/0sOvCWFmrtA?t=38633)

[Playlist with separated lessons](https://youtube.com/playlist?list=PL8VzFQ8k4U1L5QpSapVEzoSfob-4CR8zM&si=mQ3UgsmNAybRtCGh)  
[All lessons in 1 big video](https://www.youtube.com/watch?v=0sOvCWFmrtA)  
[Repo with code from course app](https://github.com/Sanjeev-Thiyagarajan/fastapi-course/)

https://fastapi.tiangolo.com/tutorial/first-steps/

[pgAdmin](http://127.0.0.1:5050/)
- create server

npz_db
- 5432

---
Main Tools:
- FastAPI
- Postgres
- SQLAlchemy
- Docker (docker-compose)
- Alembic

App:
- Social-media API

```
uvicorn app/main:app
fastapi dev app/main.py

pip freeze -> requirements.txt

pip install fastapi uvicorn psycopg2-binary python-dotenv sqlalchemy
# psycopg2-binary lockal -> psycopg2 in Docker

docker-compose build
docker-compose up

alembic init alembic
```

- [ ] CRUD
- [ ] Authorization


```sql
SELECT 
	users.id as user_id, 
	COUNT(owner_id) as posts
FROM posts
-- LEFT JOIN users ON posts.owner_id = users.id
RIGHT JOIN users ON posts.owner_id = users.id
GROUP BY users.id


SELECT 
	posts.id as post_id, 
	COUNT(post_id) as votes
FROM posts
LEFT JOIN votes ON votes.post_id = posts.id
GROUP BY posts.id
```