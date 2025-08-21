from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# ======= Game Accounts (In-memory) =======
accounts = {
    "minecraft": {"steve": "pickaxe123"},
    "valorant": {"jett": "dashOP"},
    "fcmobile": {"ronaldo": "goal123"}
}

# ======= Templates =======

home_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Gaming Portal</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #ff6f61, #845ec2);
            color: white;
            text-align: center;
            margin: 0;
            padding: 0;
        }
        header {
            background: rgba(0,0,0,0.3);
            padding: 20px;
            font-size: 24px;
            font-weight: bold;
        }
        nav a {
            margin: 0 15px;
            text-decoration: none;
            color: #ffd369;
            font-weight: bold;
            transition: 0.3s;
        }
        nav a:hover {
            color: #fff;
            text-shadow: 0px 0px 5px #ffd369;
        }
        .content { margin-top: 50px; }
        .game-card {
            display: inline-block;
            margin: 20px;
            padding: 20px;
            width: 200px;
            background: rgba(0,0,0,0.4);
            border-radius: 15px;
            transition: 0.3s;
        }
        .game-card:hover {
            background: rgba(0,0,0,0.6);
            transform: scale(1.05);
        }
        a.btn {
            display: block;
            margin-top: 10px;
            padding: 10px;
            background: #28a745;
            color: white;
            text-decoration: none;
            border-radius: 10px;
        }
        a.btn:hover { background: #218838; }
    </style>
</head>
<body>
    <header>
        Gaming Portal 🎮
        <nav>
            <a href="/">Home</a>
        </nav>
    </header>
    <div class="content">
        <h1>Choose Your Game</h1>
        <div class="game-card">
            <h2>Minecraft</h2>
            <a href="/login/minecraft" class="btn">Login</a>
            <a href="/create_account/minecraft" class="btn">Create Account</a>
        </div>
        <div class="game-card">
            <h2>Valorant</h2>
            <a href="/login/valorant" class="btn">Login</a>
            <a href="/create_account/valorant" class="btn">Create Account</a>
        </div>
        <div class="game-card">
            <h2>FC Mobile</h2>
            <a href="/login/fcmobile" class="btn">Login</a>
            <a href="/create_account/fcmobile" class="btn">Create Account</a>
        </div>
    </div>
</body>
</html>
"""

login_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Login - {{ game }}</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #00c9ff, #92fe9d);
            text-align: center;
            margin: 0; padding: 0;
        }
        .box {
            margin: 100px auto;
            background: rgba(255,255,255,0.2);
            padding: 30px;
            width: 300px;
            border-radius: 15px;
        }
        input, button {
            margin: 10px;
            padding: 10px;
            border-radius: 8px;
            border: none;
        }
        button {
            background: #ff6f61;
            color: white;
            cursor: pointer;
        }
        button:hover { background: #ff3b2e; }
    </style>
</head>
<body>
    <div class="box">
        <h2>Login - {{ game }}</h2>
        <form method="POST">
            <input type="text" name="username" placeholder="Username" required><br>
            <input type="password" name="password" placeholder="Password" required><br>
            <button type="submit">Login</button>
        </form>
    </div>
</body>
</html>
"""

profile_template = """
<!DOCTYPE html>
<html>
<head>
    <title>{{ game }} Profile</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #f7971e, #ffd200);
            text-align: center;
            margin: 0; padding: 0;
            color: black;
        }
        .box {
            margin: 80px auto;
            background: rgba(255,255,255,0.8);
            padding: 30px;
            width: 350px;
            border-radius: 20px;
        }
    </style>
</head>
<body>
    <div class="box">
        <h2>{{ game }} Profile</h2>
        <p><b>Username:</b> {{ username }}</p>
        <p>Welcome to the {{ game }} gaming zone! 🎮</p>
        <button onclick="window.location.href='/'">🏠 Home</button>
    </div>
</body>
</html>
"""

create_account_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Create Account - {{ game }}</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #fbc2eb, #a6c1ee);
            text-align: center;
            margin: 0; padding: 0;
        }
        .box {
            margin: 80px auto;
            background: rgba(255,255,255,0.4);
            padding: 30px;
            width: 320px;
            border-radius: 15px;
        }
        input, button {
            margin: 10px;
            padding: 10px;
            border-radius: 8px;
            border: none;
        }
        button {
            background: #28a745;
            color: white;
            cursor: pointer;
        }
        button:hover { background: #218838; }
    </style>
</head>
<body>
    <div class="box">
        <h2>Create Account - {{ game }}</h2>
        <form method="POST">
            <input type="text" name="username" placeholder="Choose Username" required><br>
            <input type="password" name="password" placeholder="Choose Password" required><br>
            <input type="password" name="confirm" placeholder="Confirm Password" required><br>
            <button type="submit">Save</button>
        </form>
    </div>
</body>
</html>
"""

# ======= Routes =======

@app.route("/")
def home():
    return render_template_string(home_template)

@app.route("/login/<game>", methods=["GET", "POST"])
def login(game):
    if request.method == "POST":
        uname = request.form.get("username")
        pwd = request.form.get("password")
        if uname in accounts[game] and accounts[game][uname] == pwd:
            return redirect(url_for("profile", game=game, username=uname))
        else:
            return "<h3 style='color:red;'>Invalid credentials!</h3>" + render_template_string(login_template, game=game)
    return render_template_string(login_template, game=game)

@app.route("/profile/<game>/<username>")
def profile(game, username):
    return render_template_string(profile_template, game=game.capitalize(), username=username)

@app.route("/create_account/<game>", methods=["GET", "POST"])
def create_account(game):
    if request.method == "POST":
        uname = request.form.get("username")
        pwd = request.form.get("password")
        confirm = request.form.get("confirm")
        if pwd == confirm:
            accounts[game][uname] = pwd
            return redirect(url_for("profile", game=game, username=uname))
        else:
            return "<h3 style='color:red;'>Passwords do not match!</h3>" + render_template_string(create_account_template, game=game)
    return render_template_string(create_account_template, game=game)

# Run App
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
