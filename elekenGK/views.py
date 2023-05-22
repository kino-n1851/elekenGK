from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from elekenGK.models import UserData, Message
import json
import uuid
import datetime

class TestView(APIView):

    def get(self, request, format=None):
        usernames = [user.name for user in UserData.objects.all()]
        return Response(usernames)

class AccessView(APIView):
    def post(self, request, format=None):
        content = ""
        params = request.data
        iDm = params.get("nfc_iDm", "")
        target_user = UserData.objects.get_or_none(nfc_iDm=iDm)
        if not target_user:
            temp_users = [user for user in UserData.objects.all() if user.is_temporary]
            if not temp_users:
                print("there are no temp users")
                return Response()
            
            if len(temp_users) > 1:
                for temp_user in temp_users:
                    temp_user.delete()
                print("[NFC]登録待ちリスト不正")
                errorMessage = "不正な形式の登録待ちリストが検出されました。\n受付リストを削除しました。"
                message = Message.objects.all()[0]
                message.content = errorMessage
                message.version_id = str(uuid.uuid5(uuid.uuid1(), "tekitoSolt"))
                message.save()
                content = {"content":errorMessage}
                return Response(content)
            
            datetime_now = datetime.datetime.now(datetime.timezone.utc)
            if datetime_now > temp_users[0].register_expiration_date:
                print("[NFC]受付時間切れ")
                errorMessage = "NFC受付時間切れです。\n再度登録手続きをお願いします。"
                message = Message.objects.all()[0]
                message.content = errorMessage
                message.version_id = str(uuid.uuid5(uuid.uuid1(), "tekitoSolt"))
                message.save()
                content = {"content":errorMessage}
                return Response(content)
            
            target_user = temp_users[0]
            target_user.nfc_iDm = iDm
            target_user.is_temporary = False
            target_user.is_active = False
            content = f"{target_user.name} の本登録に成功しました。\n"

        
        datetime_now = datetime.datetime.now(datetime.timezone.utc)
        passed_time = datetime_now - target_user.last_touch_time
        ignore_interval = datetime.timedelta(minutes=1)
        if passed_time <= ignore_interval:
            print("touch Ignored.")
            return Response()
        
        if not [user for user in UserData.objects.all() if user.is_active]:
            content += f"{target_user.name} が鍵を開けました。\n -----------------\n"
        target_user.is_active = not target_user.is_active
        target_user.save()
        if not [user for user in UserData.objects.all() if user.is_active]:
            content += f"{target_user.name} が鍵を閉めました。\n"

        if(target_user.is_active):
            print(f"{target_user.name} login.")
        else:
            print(f"{target_user.name} logout.")
        target_user.last_touch_time = datetime_now
        target_user.save()
        
        active_icon = "\N{Large Green Circle}"
        inActive_icon = "\N{Medium White Circle}"
        active_users = [user.name for user in UserData.objects.all() if user.is_active]
        always_visible_users = [user.name for user in UserData.objects.all() if user.is_always_visible]
        visible_unactive_users = list(set(always_visible_users) - set(active_users))
        
        #print(f"{content=}")
        for username in active_users:
            content += "{:20} {} \n".format(username, active_icon)
        
        if active_users and visible_unactive_users: 
            content += "--------------\n"
    
        for username in visible_unactive_users:
            content += "{:20} {} \n".format(username, inActive_icon)
        #print(f"{content=}")
        
        message = Message.objects.all()[0]
        message.content = content
        message.version_id = str(uuid.uuid5(uuid.uuid1(), "tekitoSolt"))
        message.save()
        return Response()

class DiscordMessageView(APIView):
    def get(self, request, format=None):
        messages = [message for message in Message.objects.all()]
        if (len(messages) >= 2):
            print("too many message registered!!")
        if (len(messages) < 1):
            print("message object has not registered!")
        if(messages):
            message_id = messages[0].message_id
            channel_id = messages[0].channel_id
            uid = messages[0].version_id
            content = messages[0].content
            json_content = {
                'channel_id':channel_id,
                'message_id':message_id,
                'version_id':uid,
                'content':content,
            }
            return Response(json_content)
        else:
            return Response({"content": "[error] message object may broken.",})
    
    def post(self, request, format=None):
        params = request.data
        message = Message.objects.all()[0]#err
        if params.get("message_id", "") and params.get("channel_id", ""):
            message.message_id = params.get("message_id", "")
            message.channel_id = params.get("channel_id", "")
            message.version_id = str(uuid.uuid5(uuid.uuid1(), "tekitoSolt"))
            message.save()
        else:
            print("discord IDs are invalid!!")
        return Response()

class CreateTempUserView(APIView):
    def post(self, request, format=None):
        params = request.data
        name = params.get("name", "")
        discord_id = params.get("discord_id", "")
        is_always_visible = bool(params.get("is_core", ""))
        if(not name or not discord_id):
            print("userCreate: parameter not found!")
            return Response({"content":"[error] something went wrong!"})

        temp_users = [user for user in UserData.objects.all() if user.is_temporary]
        datetime_now = datetime.datetime.now(datetime.timezone.utc)
        for temp_user in temp_users:
            if datetime_now > temp_user.register_expiration_date:
                temp_user.delete()
        temp_users = [user for user in UserData.objects.all() if user.is_temporary]
        if temp_users:
            content = {'content':"[error] 別アカウントのNFC登録受付中です。\n数分後にもう一度作成してください。"}
            return Response(content)
        
        target_user = UserData.objects.get_or_none(discord_id=discord_id)
        if target_user:
            target_user.is_temporary = True
            target_user.is_always_visible = is_always_visible
            expire_date = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=3)
            target_user.register_expiration_date = expire_date
            target_user.save()
            content = {"content":"NFC受付時間を更新しました。\n3分以内にNFCリーダーにタッチしてください。"}
            return Response(content)
        
        datetime_now = datetime.datetime.now(datetime.timezone.utc)
        expire_date = datetime_now + datetime.timedelta(minutes=3)
        new_user = UserData.objects.create(name=name, discord_id=discord_id, nfc_iDm="temporary", is_temporary=True, is_always_visible=is_always_visible, register_expiration_date=expire_date)
        content = {"content":"仮登録に成功しました。\n3分以内にNFCリーダーにタッチしてください。"}
        return Response(content)

class AllUserLogoutView(APIView):
    def post(self, request, format=None):
        for user in UserData.objects.all():
            user.is_active = False
            user.save()
        return Response()

class UpdateUserNameView(APIView):
    def post(self, request, format=None):
        params = request.data
        discord_id = params.get("discord_id","")
        name = params.get("name","")
        if not discord_id:
            return Response({"content":"[error] ユーザIDが受信できませんでした。"})
        target_user = UserData.objects.get_or_none(discord_id=discord_id)
        if not target_user:
            return Response({"content":"[error] IDに対応したユーザが見つかりませんでした。"})
        
        target_user.name = name
        target_user.save()
        return Response({"content":"ユーザ名の変更を受け付けました。\n次回の更新から新しいユーザ名が反映されます。"})
        
      
    
    
