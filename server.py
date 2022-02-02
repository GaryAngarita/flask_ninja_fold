from flask import Flask, render_template, request, redirect, session, message_flashed
import random
from tkinter import messagebox
app = Flask(__name__)
app.secret_key = 'I Am Inevitable!'

@app.route('/')
def index():
    if 'gold' not in session and 'count' not in session:        
        session['count'] = 0
        session['gold'] = 0
        session['activity'] = []
        activities = session['activity']
    else:
        activities = session['activity']
    return render_template('ninja.html', activities=activities)

@app.route('/process_money', methods=['POST'])
def process_money():
    print(session['gold'])
    print(request.form)
    if 'gold' in session and 'count' in session:
        activities = session['activity']
        count = session['count']
        gold = session['gold']
        location = request.form['location']
        if location == 'farm':
            gold += random.randrange(10, 20)
            session['gold'] = gold
        if location == 'cave':
            gold += random.randrange(5, 10)
            session['gold'] = gold
        if location == 'house':
            gold += random.randrange(2, 5)
            session['gold'] = gold
        str = f'{count+1}. You have earned {abs(gold)} gold!'
        if location == 'casino':
            new_gold = random.randrange(-50, 50)
            gold += new_gold
            if new_gold > 0:
                str = f'{count+1}. You have earned {new_gold} gold!'
                session['gold'] = gold
            elif new_gold < 0:
                str = f'{count+1}. You have lost {abs(new_gold)} gold!'
                session['gold'] = gold
            else:
                str = f'{count+1}. You broke even - {new_gold} gold. What are the chances?'
                session['gold'] = gold
        
        print(session['gold'])
        gold = session['gold']
        session['count'] = count+1
        count = session['count']
        activities.insert(0, str)
        print(activities)
        print(session['count'])
        session['activity'] = activities
        if session['count'] <= 25 and session['gold'] >= 250:
            messagebox.showinfo('Winner', f'You earned {gold} gold in {count} moves!')
        elif session['count'] > 25:
            messagebox.showerror('Loser', f'You only earned {gold} gold in {count} moves :( Try again')
        return redirect('/')
    else:
        return redirect('/')

@app.route('/reset')
def destroy():
    session.clear()
    return redirect('/')

if __name__=="__main__":
    app.run(debug=True)