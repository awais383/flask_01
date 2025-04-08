# from flask import Flask, render_template
# app= Flask(__name__)
# @app.route("/")
# def Hello_World():
#     # return render_template("index.html")
#     return "<h1>Hello World</h1>"
# app.run(debug=True)






from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>This is my first Flask program</h1>"

@app.route("/second")
def second():
    return "<h2>This is my second Flask program</h2>"

@app.route("/success/<int:score>")
def success(score):
    # return f"The person has passed by scoring: {score}"
    return "The person has passed by scoring: " +str(score)

@app.route("/fail/<int:score>")
def fail(score):
    return "The person has fail by scoring: " +str(score)

@app.route("/form", methods= ["GET", "POST"])
def form():
    if request.method== "GET":
        return render_template("form.html")
    else:
        maths= float(request.form["maths"])
        science= float(request.form["science"])
        history= float(request.form["history"])

        average= (maths+ science+ history) /3

        result = "success" if average > 50 else "fail"
        return redirect(url_for(result, score=average))

        return render_template("form.html", score= average) 

if __name__ == "__main__":

    # debug= true automatically update the browser
    app.run(debug=True)
