from flask import Flask, jsonify, render_template, request, abort
from flask import current_app as app
from app.models import User, Chat, ChatUser, Message
from . import db
import ast

@app.route('/login', methods=['GET'])
def login():
    return "Login portal"

@app.route('/api/chats', methods=['GET'])
def get_chats():
    """
    Returns chats for a given user_id
    """

    result_proxy = db.session.execute(
        '''
        SELECT
          c.id
         ,c.name
         ,c.created_at
         ,c.updated_at
        FROM
          chats AS c
        INNER JOIN
          chat_users AS cu
        ON
          cu.chat_id = c.id
        WHERE
          cu.user_id = :user_id
        ORDER BY
          c.updated_at DESC
        ''',dict(user_id=request.args['user_id'])
          )
    result = [Chat.from_dict(r).to_dict() for r in result_proxy]
    return jsonify(result)

@app.route('/api/chats', methods=['POST'])
def create_chat():
    """
    Create a chat for a given user_id
    """
    chat = Chat.from_dict(request.json)
    chat_user = ChatUser.from_dict(request.json, request.args(['user_id']))
    query_1 = db.session.execute(
        '''
        INSERT INTO chats (name)
        VALUES (name)
        RETURNING id
        ON CONFLICT DO NOTHING
        '''
        , dict(name=chat.name)
    )
    
    query_2 = db.session.execute(
        '''
        INSERT INTO chat_users (user_id, chat_id)
        VALUES (:user_id, :chat_id)
        '''
        , dict(user_id=request.args['user_id'], chat_id=1)
    )
    db.session.commit()


@app.route('/api/chats/<chat_id>/messages', methods =['GET'])
def get_messages(chat_id):
    """
    Gets all the messages for a user_id and chat_id
    """

    greater_than_message_id = request.args.get('greater_than_message_id', 0)
    result_proxy = db.session.execute(
        '''
        SELECT 
          m.id
         ,m.chat_id
         ,m.sender_id
         ,m.content
         ,m.created_at
         ,CASE WHEN m.sender_id = :user_id THEN TRUE ELSE FALSE END AS sent
        FROM 
          messages AS m 
        INNER JOIN 
          chat_users AS gu 
        ON 
          gu.chat_id = m.chat_id 
        WHERE 
          m.chat_id = :chat_id 
        AND
          m.id > :greater_than_message_id
        AND 
          gu.user_id = :user_id
        GROUP BY
          1,2,3,4,5
        ORDER BY
          created_at DESC
        '''
        , dict(greater_than_message_id=greater_than_message_id, chat_id=chat_id, user_id=int(request.args['user_id'])))
    result = []
    for r in result_proxy:
        result.append({
          'id': r[0],
          'chat_id': r[1],
          'sender_id': r[2],
          'content': r[3],
          'created_at': r[4]
        })

    return jsonify(result)

@app.route('/api/chats/<chat_id>/messages', methods =['POST'])
def send_message(chat_id):
    """
    Allows a user to send a message. Takes as arguments chat_id, sender_id and sender
    """
    #
    if request.json: # If there is data in the POST request
        # message = Message.from_dict(request.json, chat_id, request.args['user_id'])

        result_proxy = db.session.execute(
            '''
            INSERT INTO 
              messages (chat_id, sender_id, content) 
            VALUES 
              (:chat_id, :sender_id, :content)
            RETURNING id, chat_id, sender_id, content, created_at
            '''
        , dict(chat_id=int(chat_id), sender_id=int(request.args['user_id']), content=request.json['content'])
        )

        result = result_proxy.fetchone()


        db.session.commit()

        return jsonify({'id': result[0],
        'chat_id': result[1],
        'sender_id': result[2],
        'content': result[3],
        'created_at': result[4]
        })
    else:
        return "Error"

@app.route('/api/chats/<chat_id>/messages', methods =['DELETE'])
def delete_message(chat_id):
    """
    Delete a message.
    """
    if request.json:
        for row in request.json:
            message = Message.from_messages(row, chat_id, request.args['user_id'])
            db.session.execute(
                '''
                DELETE FROM
                  messages
                WHERE
                  id = :message_id
                '''
                , dict(message_id=message.id)
            )
        db.session.commit()
        return "Successfully deleted message"
    else:
        return "Error"


@app.route('/chats', methods=['GET'])
def chats():
    result_proxy = db.session.execute(
        '''
        WITH A AS(
            SELECT
              chat_id
             ,LAST_VALUE (content) OVER (PARTITION BY chat_id ORDER BY created_at RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS content
            FROM
              messages
            GROUP BY
              chat_id
             ,content
             ,created_at
        )

        SELECT
          c.id
         ,c.name
         ,c.created_at
         ,c.updated_at
         ,A.content
         ,cu.user_id
        FROM
          chats AS c
        INNER JOIN
          chat_users AS cu
        ON
          cu.chat_id = c.id
        LEFT JOIN
          A
        ON
          A.chat_id = c.id
        WHERE
          cu.user_id = :user_id
        GROUP BY
          1,2,3,4,5,6
        ORDER BY
          c.updated_at DESC
        ''',dict(user_id=request.args['user_id']))

    chats = []
    for r in result_proxy:
        chats.append(r)

    return render_template('chat.html', chats=chats, user=dict(id=request.args['user_id']))








