require 'openssl'
require 'webrick'
require 'base64'
require 'json'
require 'zlib'
require 'pry'

def encrypt(data)
  cipher = OpenSSL::Cipher::AES.new(128, :CTR)
  cipher.encrypt
  key = cipher.random_key
  iv = cipher.random_iv
  cipher.auth_data = ""
  encrypted = cipher.update(data) + cipher.final
  return encrypted
end

def get_auth(user)
  data = [user, "flag:"+File.read("flag.key").strip]
  json = JSON.dump(data)
  zip = Zlib.deflate(json)
  return Base64.strict_encode64(encrypt(zip))
end

class Srv < WEBrick::HTTPServlet::AbstractServlet
  def do_GET(req,resp)
    user = req.query["user"] || "fnord"
    resp.body = "Hallo #{user}"
    resp.status = 200
    puts get_auth(user).inspect
    cookie = WEBrick::Cookie.new("auth", get_auth(user))
    resp.cookies << cookie
    return resp
  end
end

srv = WEBrick::HTTPServer.new({Port: 12336})
srv.mount "/",Srv
srv.start
