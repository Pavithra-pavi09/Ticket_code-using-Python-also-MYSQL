import mysql.connector
import smtplib
import random
import datetime

x = datetime.datetime.now()
current = x.strftime("%H:%M:%S %p")
f=open("bill.txt","a")
f.write("\n***SUPER MARKET**\n")
f.write(f"\nTime of Purchase is {current}\n")

mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345678",
    database="movie_booking_db"
)

mycursor=mydb.cursor()

GST_RATE = 0.18  # 18% GST

def calculate_total_amount(price, quantity):
    subtotal = price * quantity
    gst_amount = subtotal * GST_RATE
    total_amount = subtotal + gst_amount
    return total_amount

def book_ticket(movie_id, customer_email, quantity):
    try:
        # Get the price of the movie
        mycursor.execute("SELECT price FROM movies WHERE id = %s", (movie_id,))
        movie = mycursor.fetchone()
        if not movie:
            print("Movie not found")
            return
        
        price = movie[0]
        total_amount = calculate_total_amount(price, quantity)
        
        # Insert booking into the bookings table
        mycursor.execute(
            "INSERT INTO bookings (movie_id, customer_email, quantity, total_amount) VALUES (%s, %s, %s, %s)",
            (movie_id, customer_email, quantity, total_amount)
        )
        mydb.commit()
        
        print("Booking recorded successfully")
        
        # Send confirmation email
        email_sending(customer_email, 'Movie Ticket Booking Confirmation', f'Your booking has been confirmed. Total amount: ${total_amount:.2f}')
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        
    finally:
       mydb.close

def email_sending(total):
    try:
        receiver_mails=["durpavadhaarani@gmail.com"]
        for i in receiver_mails:
            otp_number=random.randint(0000,9999)
            print(i,otp_number)
            s=smtplib.SMTP('SMTP.gmail.com',587)
            s.starttls()
            s.login("adipavi2005@gmail.com","aryn vqxl iupq oxet")
            message=f" your otp number is {otp_number}"
            s.sendmail("adipavi2005@gmail.com",i,message)
            s.quit()
            print("mail sent successfully")
    except:
        print("mail not sent")  