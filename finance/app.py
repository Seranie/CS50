import os
import re

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    userStocks = db.execute("SELECT symbol, SUM(shares) AS shares, cash FROM transactions JOIN users ON users.id = transactions.transaction_id WHERE transaction_id = ? GROUP BY symbol", session["user_id"])
    if len(userStocks) != 0:
        currentStockPrice = {}
        # calculate and add to dict the prices of all symbols the user owns, alongside the CURRENT value of each stock
        for row in userStocks:
            lookedup = lookup(row["symbol"])
            symbolPrice = lookedup["price"]
            currentStockPrice[row["symbol"]] = symbolPrice
        # calculate the total price of the share * current price for each stock
        stockValues = {}
        for row in currentStockPrice:
            for line in userStocks:
                if line["symbol"] == row:
                    totalPrice = line["shares"] * currentStockPrice[row]
                    stockValues[row] = totalPrice

        # total amount of $ combining all stock values
        totalStockValue = sum(stockValues.values()) + userStocks[0]["cash"]
        username = db.execute("SELECT username FROM users WHERE id = ?", session['user_id'])
        username = username[0]['username']
        cash = userStocks[0]['cash']
        return render_template("index.html", userStocks=userStocks, currentStockPrice=currentStockPrice, stockValues=stockValues, totalStockValue=totalStockValue, username=username, cash=cash)
    else:
        query = db.execute('SELECT * FROM users WHERE id = ?', session['user_id'])
        username = query[0]['username']
        cash = query[0]['cash']
        return render_template('index.html', username=username, cash=cash)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        # check for empty fields or incorrect symbol name
        if not request.form.get("symbol") or lookup(request.form.get("symbol")) == None:
            return apology("Invalid symbol")
        if not request.form.get("shares"):
            return apology("Invalid Shares")

        # check for illegal characters
        shares = request.form.get('shares')
        str = '\D+'
        regex = re.search(str, shares)
        if regex:
            return apology('Invalid shares')

        # check share for positivity
        if int(request.form.get("shares")) <= 0:
            return apology("Invalid Shares")

        symbolPrice = lookup(request.form.get("symbol"))
        symbolPrice = symbolPrice["price"]
        totalSymbolPrice = symbolPrice * int(request.form.get("shares"))
        userCash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"] )
        if userCash[0]["cash"] > totalSymbolPrice:
            # transaction happens
            now = datetime.now()
            dateStr = now.strftime("%Y-%m-%d %H:%M:%S")
            db.execute("INSERT INTO transactions VALUES(?, ?, ?, ?, ?, ?)", session["user_id"], request.form.get("symbol"), int(request.form.get("shares")), symbolPrice, totalSymbolPrice, dateStr)
            newCash = userCash[0]["cash"] - totalSymbolPrice
            db.execute("UPDATE users SET cash = ? WHERE id = ?", newCash, session["user_id"])
            # update stock table
            numberOfShares = db.execute("SELECT SUM(shares) AS shares FROM transactions WHERE transaction_id = ? AND symbol = ?", session["user_id"], request.form.get("symbol"))
            totalNumberShares = numberOfShares[0]['shares']
            checkForInsertion = db.execute("SELECT * FROM stock WHERE stock_id = ? AND symbol = ?", session['user_id'], request.form.get('symbol'))
            if len(checkForInsertion) == 0:
                db.execute("INSERT INTO stock VALUES (?, ?, ?)", session['user_id'], request.form.get('symbol'), int(request.form.get('shares')))
            else :
                db.execute("UPDATE stock SET shares = ? WHERE stock_id = ? AND symbol = ?", totalNumberShares, session['user_id'], request.form.get('symbol'))
        else:
            return apology("Not enough cash")
        # TODO REDIRECT SOMEWHERE AFTER PURCHASE
        return redirect("/")
    else:
        return render_template("buy.html")
    return apology("TODO")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    userHistory = db.execute("SELECT * FROM transactions WHERE transaction_id = ? ORDER BY transactionTime DESC", session['user_id'])
    if len(userHistory) == 0:
        return redirect('/buy')
    return render_template("history.html", userHistory=userHistory)

    return apology("TODO")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect('/')

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")
    else:
        if not request.form.get("symbol"):
            return apology("Invalid symbol")
        stock = lookup(request.form.get("symbol"))
        if stock == None:
            return apology("Invalid symbol")
        return render_template("quoted.html", stock=stock)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # if user get here through submitting registration
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("Username field is blank")
        if not request.form.get("password") or not request.form.get("confirmation"):
            return apology("Password not provided")
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords do no match")
        # require special character
        password = request.form.get('password')
        pattern = '[#?!@$%^&*-]+'
        regex = re.search(pattern, password)
        if not regex:
            return apology('Password must contain at least 1 special character')
        dbQuery = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if len(dbQuery) != 0:
            return apology("username already in use")
        else:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get("username"), generate_password_hash(request.form.get("password")))
            return redirect("/login")

    # if user gets here through get
    else:
        return render_template("register.html")




@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        # check if symbol is inputted
        if not request.form.get("symbol"):
            return apology("Invalid symbol")
        if not request.form.get("shares"):
            return apology("Invalid shares")

        # check for illegal characters
        shares = request.form.get('shares')
        str = '\D+'
        regex = re.search(str, shares)
        if regex:
            return apology('Share amount must contain only numbers')

        # check for positive share input
        if int(request.form.get("shares")) <= 0:
            return apology("Invalid share amount")

        # check if user owns the symbol stock server side
        userStocks = db.execute("SELECT * FROM stock WHERE stock_id = ? AND symbol = ?", session["user_id"], request.form.get('symbol'))
        if len(userStocks) == 0:
            return apology("You Dont Own that Stock Dumbo")

        # check amount of shares attempting to sell
        if userStocks[0]['shares'] < int(request.form.get('shares')):
            return apology('You dont own that many shares')

        shares = int(request.form.get('shares')) * -1
        sharePrice = lookup(request.form.get('symbol'))
        sharePrice = sharePrice['price']
        now = datetime.now()
        now = now.strftime("%Y-%m-%d %H:%M:%S")
        db.execute("INSERT INTO transactions VALUES (?, ?, ?, ?, ?, ?)", session['user_id'], request.form.get('symbol'), shares, sharePrice, sharePrice * int(request.form.get('shares')), now)
        db.execute("UPDATE stock SET shares = (SELECT shares FROM stock WHERE stock_id = ? AND symbol = ?) + ? WHERE stock_id = ? AND symbol = ?", session['user_id'], request.form.get('symbol'), shares, session['user_id'], request.form.get('symbol') )
        totalSharePrice = sharePrice * int(request.form.get('shares'))
        db.execute("UPDATE users SET cash = (SELECT cash FROM users WHERE id = ?) + ? WHERE id = ?", session['user_id'], totalSharePrice, session['user_id'])

    else:
        allStocks = db.execute("SELECT * FROM stock WHERE stock_id = ?", session['user_id'])
        return render_template('sell.html', allStocks=allStocks)
    return redirect('/')



@app.route("/changepassword", methods=["GET", "POST"])
@login_required
def changePassword():
    if request.method == 'POST':
        # Check if current password input is correct
        currentPassword = request.form.get("currentPassword")
        dbPassword = db.execute("SELECT hash FROM users WHERE id = ?", session['user_id'])
        dbPasswordHash = dbPassword[0]['hash']
        if not check_password_hash(dbPasswordHash, currentPassword):
            return apology('Incorrect Password')
        # Check new password
        newPassword = request.form.get('newPassword')
        confirmationPassword = request.form.get('confirmation')
        pattern = '[#?!@$%^&*-]+'
        regex = re.search(pattern, newPassword)
        if not regex:
            return apology('Password must contain at least 1 special character')
        if newPassword != confirmationPassword:
            return apology('New passwords do not match')
        if currentPassword == newPassword:
            return apology('New Password must be different')
        newPasswordHash = generate_password_hash(newPassword)
        db.execute("UPDATE users SET hash = ? WHERE id = ?", newPasswordHash, session['user_id'])
        session['user_id'] = None
        return redirect('/')
    else:
        return render_template("changePassword.html")


@app.route('/addcash', methods=["GET", "POST"])
@login_required
def addcash():
    if request.method == 'POST':
        cash = request.form.get('cash')
        if int(cash) <= 0:
            return apology('Cash input must be positive number')
        # check for alphabets in cash amount
        str = '[^\d\.]+'
        regex = re.search(str, cash)
        if regex:
            return apology('Cash amount must contain only numbers')

        query = db.execute('SELECT cash FROM users WHERE id= ?', session['user_id'])
        currentCash = query[0]['cash']
        newCash = currentCash + int(cash)
        password = request.form.get('password')
        dbQuery = db.execute('SELECT hash FROM users WHERE id = ?', session['user_id'])
        hash = dbQuery[0]['hash']
        if check_password_hash(hash, password):
            db.execute("UPDATE users SET cash = ? WHERE id = ?", newCash, session['user_id'])
        else:
            return apology('Incorrect Password')
        return redirect('/')
    else:
        cash = request.args.get('cash')
        if not cash:
            return apology('Input cash')
        if int(cash) <= 0:
            return apology('Invalid amount')

        # check if cash is numerical
        str = '[^\d\.]+'
        regex = re.search(str, cash)
        if regex:
            return apology('Cash amount must contain only numbers')

        return render_template('addcash.html', amountToAdd=cash)


@app.route('/indexTransaction', methods=['GET','POST'])
@login_required
def indextransactionbuy():
    if request.method == "POST":
        transactionType = request.form.get('btn')
        if transactionType == 'Buy':
            return redirect('/buy', code=307)
        elif transactionType == 'Sell':
            return redirect('/sell', code=307)
    else:
        return redirect('/')

