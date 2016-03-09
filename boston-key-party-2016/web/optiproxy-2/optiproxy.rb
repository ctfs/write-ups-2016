require 'nokogiri'
require 'open-uri'
require 'sinatra'
require 'shellwords'
require 'base64'
require 'fileutils'

set :bind, "0.0.0.0"
cdir = Dir.pwd
get '/' do
	str = "welcome to the automatic resource inliner, we inline all images"
	str << " go to /example.com to get an inlined version of example.com"
	str << " flag is in /flag"
	str << " source is in /source"
	str
end

get '/source' do
	IO.read cdir + "/" + $0
end

get '/flag' do
	str = "I mean, /flag on the file system... If you're looking here, I question"
	str << " your skills"
	str
end

get '/:url' do
	url = params[:url]
	main_dir = Dir.pwd
	temp_dir = ""
	dir = Dir.mktmpdir "inliner"
	Dir.chdir dir
	temp_dir = dir
	exec = "timeout 2 wget -T 2 --page-requisites #{Shellwords.shellescape url}"
	`#{exec}`
	my_dir = Dir.glob ("**/")
	Dir.chdir my_dir[0]
	index_file = "index.html"
	html_file = IO.read index_file
	doc = Nokogiri::HTML(open(index_file))
	doc.xpath('//img').each do |img|
		header = img.xpath('preceding::h2[1]').text
		image = img['src']
		img_data = ""
		uri_scheme = URI(image).scheme
		begin
			if (uri_scheme == "http" or uri_scheme == "https")
				url = image
			else
				url = "http://#{url}/#{image}"
			end
			img_data = open(url).read
			b64d = "data:image/png;base64," + Base64.strict_encode64(img_data)
			img['src'] = b64d
		rescue
			# gotta catch 'em all
			puts "lole"
			next
		end
	end
	FileUtils.rm_rf dir
	Dir.chdir main_dir
	doc.to_html
end
