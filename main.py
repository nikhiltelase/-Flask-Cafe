from flask import Flask, render_template, redirect
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField, SelectField
from wtforms.validators import DataRequired, URL
import csv


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
bootstrap = Bootstrap5(app)


class CafeForm(FlaskForm):
    name = StringField('Cafe name', validators=[DataRequired()])
    location_url = URLField("Cafe location on google map",
                            validators=[DataRequired(), URL()],
                            )
    open_time = StringField("Opening Time e.g.8AM", validators=[DataRequired()])
    close_time = StringField("Closing Time e.g.10PM", validators=[DataRequired()])
    coffee_rating = SelectField('Coffee Rating', choices=[
        ('☕', '☕️'),
        ('☕️☕️', '☕️☕️'),
        ('☕️☕️☕️', '☕️☕️☕️'),
        ('☕️☕️☕️☕️', '☕️☕️☕️☕️'),
        ('☕️☕️☕️☕️☕️', '☕️☕️☕️☕️☕️')
    ], validators=[DataRequired()],)
    wifi_strength = SelectField('Wifi Strength Rating', choices=[
        ('💪', '💪'),
        ('💪💪', '💪💪'),
        ('💪💪💪', '💪💪💪'),
        ('💪💪💪💪', '💪💪💪💪'),
        ('💪💪💪💪💪', '💪💪💪💪💪'),
    ], validators=[DataRequired()],)
    power_socket = SelectField('Power Socket Availability', choices=[
        ('🔌', '🔌'),
        ('🔌🔌', '🔌🔌'),
        ('🔌🔌🔌', '🔌🔌🔌'),
        ('🔌🔌🔌🔌', '🔌🔌🔌🔌'),
        ('🔌🔌🔌🔌🔌', '🔌🔌🔌🔌🔌')
    ], validators=[DataRequired()],)
    submit = SubmitField('Submit')


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        cafe = form.data
        row = (f"{cafe['name']},"
               f"{cafe['location_url']},"
               f"{cafe['open_time']},"
               f"{cafe['close_time']},"
               f"{cafe['coffee_rating']},"
               f"{cafe['wifi_strength']},"
               f"{cafe['power_socket']}")
        with open("cafe-data.csv", "a", encoding="utf-8") as file:
            file.writelines(f"\n{row}")
        return redirect("/cafes")

    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
        print(list_of_rows)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
