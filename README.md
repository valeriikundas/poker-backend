this api implements 2 things:

1. table and user management
2. game related stuff

table management consists of

- authentication
- players joining and leaving table

game related stuff is the minimal version. all work should be done by game server and clients
backend should just do mailing between game server and clients.

- inform player - send info to one player at the table - ws
- inform players - send info to all players at the table - ws
- request_action from player - send request for move - ws
- act - apply move from player - resend it to game server - http
