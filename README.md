# allegro-bot

Bot downloads orders from allegro.pl with Allegro Api and sends items in game (Tibia) to buyer.

<b>AllegroToken.py</b> - used to generate token connected to Allegro acount - need to do it first, then <b>RefreshToken.py</b> will renewal it with each getting new orders (stores it in <b>access_tokens_allegro.txt</b> - both, refresh token and access token) .

<b>AllegroOrder.py</b> - gets orders from Allegro, checks message from seller, verifies if everything is ok (nick, world, auction id - by <b>AuctionIdServers</b>, <b>Names_char</b>, first/second/third replace), forwards to <b>main.py</b> to send items.

After that, carries out the orders, save screenshots to <b>Zrealizowane</b>, count profit etc., adds a record to the database.
