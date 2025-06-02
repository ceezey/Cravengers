from .login import login_required
from . import get_db
from flask import (
    Blueprint, render_template, request,
    session, redirect, url_for, send_file, flash
)

main = Blueprint('main', __name__)

@main.route('/')
def home():
    '''
    redirect user to index.html ie sign-in page
    '''
    return redirect(url_for('main.homepage'))


@main.route('/index.html')
def index():
    '''
    renders login page
    '''
    return render_template('index.html')

@main.route('/homepage.html')
def homepage():
    '''
    renders home page
    '''
    return render_template('homepage.html')

@main.route("/sign-up.html")
def sign_up():
    return render_template("sign-up.html")

# Route to serve image file
@main.route('/home')
def get_home_image():
    filename = '../templates/assets/home.png'  # Path to your image file
    return send_file(filename, mimetype='image/png')

@main.route('/search')
def get_search_image():
    filename = '../templates/assets/search.png' # Path to your image file
    return send_file(filename, mimetype='image/png')

@main.route('/user')
def get_user_image():
    filename = '../templates/assets/user.png'  # Path to your image file
    return send_file(filename, mimetype='image/png')

@main.route('/logo')
def get_logo_image():
    filename = '../templates/assets/logo.png'  # Path to your image file
    return send_file(filename, mimetype='image/png')

@main.route('/cravengers')
def get_cravengers_image():
    filename = '../templates/assets/cravengers.png'  # Path to your image file
    return send_file(filename, mimetype='image/png')

@main.route('/cravengers-noshadow')
def get_cravengers_noshadow_image():
    filename = '../templates/assets/cravengers-nshadow.png'  # Path to your image file
    return send_file(filename, mimetype='image/png')

# homepage assets
@main.route('/controller')
def get_controller_image():
    filename = '../templates/assets/controller.png'  # Path to your image file
    return send_file(filename, mimetype='image/png')

@main.route('/eco')
def get_eco_image():
    filename = '../templates/assets/eco.png'  # Path to your image file
    return send_file(filename, mimetype='image/png')

@main.route('/location')
def get_location_image():
    filename = '../templates/assets/location.png'  # Path to your image file
    return send_file(filename, mimetype='image/png')

@main.route('/rider')
def get_rider_image():
    filename = '../templates/assets/rider.png'  # Path to your image file
    return send_file(filename, mimetype='image/png')

@main.route('/food')
def get_food_image():
    filename = '../templates/assets/food.png'  # Path to your image file
    return send_file(filename, mimetype='image/png')

@main.route('/trophy')
def get_trophy_image():
    filename = '../templates/assets/trophy.png'  # Path to your image file
    return send_file(filename, mimetype='image/png')

@main.route('/letter')
def get_letter_image():
    filename = '../templates/assets/letter.png'  # Path to your image file
    return send_file(filename, mimetype='image/png')

@main.route('/founders')
def get_founders_image():
    filename = '../templates/assets/founders.png'  # Path to your image file
    return send_file(filename, mimetype='image/png')


@main.route("/adminpage.html")
def adminpage():
    # update session info every time
    user_info = session.get('user_info')
    UID = user_info['UID']
    db = get_db()
    user_info = db.cursor().execute(
        """ select *
            from Users
            where UID = ?""", (UID,)
    ).fetchone()
    session['user_info'] = dict(user_info)

    # fetch shop_info
    shop_info = db.cursor().execute(
        """ select *
            from Stores
            where S_owner = ?""", (UID,)
    ).fetchone()

    # fetch product_info
    product_info = db.cursor().execute(
        """ select *
            from Products
            where P_owner = ?""", (UID,)
    ).fetchall()

    costumer_info = db.cursor().execute(
        """ select *
            from Users"""
    ).fetchall()

    image_info = [tple['P_image'].decode("utf-8") for tple in product_info]

    return render_template("adminpage.html", user_info=user_info, shop_info=shop_info, product_info=product_info, image_info=image_info, costumer_info=costumer_info)



@main.route("/userpage.html")
@login_required
def userpage():
    # update session info every time
    user_info = session.get('user_info')
    UID = user_info['UID']
    db = get_db()
    user_info = db.cursor().execute(
        """ select *
            from Users
            where UID = ?""", (UID,)
    ).fetchone()
    session['user_info'] = dict(user_info)

    # fetch shop_info
    shop_info = db.cursor().execute(
        """ select *
            from Stores
            where S_owner = ?""", (UID,)
    ).fetchone()

    # fetch product_info
    product_info = db.cursor().execute(
        """ select *
            from Products
            where P_owner = ?""", (2,)
    ).fetchall()

    image_info = [tple['P_image'].decode("utf-8") for tple in product_info]

    return render_template("userpage.html", user_info=user_info, shop_info=shop_info, product_info=product_info, image_info=image_info)



@main.route("/productlistpage.html")
@login_required
def productlistpage():
    # update session info every time
    user_info = session.get('user_info')
    UID = user_info['UID']
    db = get_db()
    user_info = db.cursor().execute(
        """ select *
            from Users
            where UID = ?""", (UID,)
    ).fetchone()
    session['user_info'] = dict(user_info)

    # fetch shop_info
    shop_info = db.cursor().execute(
        """ select *
            from Stores
            where S_owner = ?""", (UID,)
    ).fetchone()

    # fetch product_info
    product_info = db.cursor().execute(
        """ select *
            from Products
            where P_owner = ?""", (2,)
    ).fetchall()

    image_info = [tple['P_image'].decode("utf-8") for tple in product_info]

    return render_template("productlistpage.html", user_info=user_info, shop_info=shop_info, product_info=product_info, image_info=image_info)


@main.route("/profilepage.html")
@login_required
def profilepage():
    # update session info every time
    user_info = session.get('user_info')
    UID = user_info['UID']
    db = get_db()
    user_info = db.cursor().execute(
        """ select *
            from Users
            where UID = ?""", (UID,)
    ).fetchone()
    session['user_info'] = dict(user_info)

    # fetch shop_info
    shop_info = db.cursor().execute(
        """ select *
            from Stores
            where S_owner = ?""", (UID,)
    ).fetchone()

    # fetch product_info
    product_info = db.cursor().execute(
        """ select *
            from Products
            where P_owner = ?""", (2,)
    ).fetchall()

    image_info = [tple['P_image'].decode("utf-8") for tple in product_info]

    return render_template("profilepage.html", user_info=user_info, shop_info=shop_info, product_info=product_info, image_info=image_info)


@main.route("/streak.html")
# @login_required
def streak():
    # update session info every time
    # user_info = session.get('user_info')
    # UID = user_info['UID']
    # db = get_db()
    # user_info = db.cursor().execute(
    #     """ select *
    #         from Users
    #         where UID = ?""", (UID,)
    # ).fetchone()
    # session['user_info'] = dict(user_info)

    # fetch shop_info
    # shop_info = db.cursor().execute(
    #     """ select *
    #         from Stores
    #         where S_owner = ?""", (UID,)
    # ).fetchone()

    # fetch product_info
    # product_info = db.cursor().execute(
    #     """ select *
    #         from Products
    #         where P_owner = ?""", (2,)
    # ).fetchall()

    # image_info = [tple['P_image'].decode("utf-8") for tple in product_info]

    return render_template("streak.html")





# @main.route("/nav.html")
# @login_required
# def nav():
#     # update session info every time
#     user_info = session.get('user_info')
#     UID = user_info['UID']
#     db = get_db()
#     user_info = db.cursor().execute(
#         """ select *
#             from Users
#             where UID = ?""", (UID,)
#     ).fetchone()
#     session['user_info'] = dict(user_info)

#     # fetch shop_info
#     shop_info = db.cursor().execute(
#         """ select *
#             from Stores
#             where S_owner = ?""", (UID,)
#     ).fetchone()

#     # fetch product_info
#     product_info = db.cursor().execute(
#         """ select *
#             from Products
#             where P_owner = ?""", (UID,)
#     ).fetchall()

#     image_info = [tple['P_image'].decode("utf-8") for tple in product_info]

#     return render_template("nav.html", user_info=user_info, shop_info=shop_info, product_info=product_info, image_info=image_info)


# @main.route("/edit_location", methods=['POST'])
# @login_required
# def edit_location():
#     user_info = session.get('user_info')
#     UID = user_info['UID']
#     latitude = request.form['latitude']
#     longitude = request.form['longitude']

#     # check any blanks:
#     for k, v in request.form.items():
#         if v == '':
#             flash(f"Please check: '{k}' is not filled")
#             return redirect(url_for("main.nav"))

#     # check validity
#     try:
#         latitude, longitude = float(latitude), float(longitude)
#     except ValueError:
#         flash("Please check: locations can only be float")
#         return redirect(url_for("main.nav"))

#     if not (-90 <= int(latitude) <= 90 and -180 <= int(longitude) <= 180):
#         flash("Please check: locations not possible")
#         return redirect(url_for("main.nav"))

#     # update location
#     db = get_db()
#     db.cursor().execute("""
#         update Users
#         set U_latitude = ?, U_longitude = ?
#         where UID = ?
#     """, (latitude, longitude, UID))
#     db.commit()

#     return redirect(url_for('main.nav'))







