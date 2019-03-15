require 'open-uri'
require 'rexml/document'
require 'rexml/streamlistener'
require 'rubygems'
require 'cgi'
#require 'htmlentities'

include REXML


class Parser

    def Parser.parseFile(inputfilename,outputfilename,collection,afk,number)
        listener = MyListener.new(outputfilename,collection,afk,number)
        source = File.new File.expand_path(inputfilename)
        Document.parse_stream(source, listener)
        listener.closing_lines
        source.close
    end

    def Parser.parseString(id,xml,output_file,collection,afk)
        listener = MyListener.new(output_file,collection,afk,1)
        Document.parse_stream(xml, listener)
    end

end


class MyListener
    include StreamListener

    def closing_lines
        rdf_rdf =<<EOF
  </rdf:Description>

EOF
#        @output.puts rdf_rdf
#        @output.puts
    end

    def initialize(outputfile,collection,afk,number)
        @output = outputfile
        @level = 1
        @indent = ""
        @collection = collection
        @afk = afk
        @number = number
        @seq = ""
	@in_resoluties = false
	@in_postprandium = false
    end

    def zittingsdag_start attrs
        put_out "\n#{@indent}<#{@afk}:zittingsdag>"
    end

    def zittingsdag_end
    end

    def presentielijst_start attrs
        put_out "\n#{@indent}<#{@afk}:presentielijst>"
  	put_out "\n#{@indent}<rdf:Seq>"
    end

    def presentielijst_end
  	@output.puts "\n#{@indent}</rdf:Seq>"
        indent = "  " * (@level - 1)
  	put_out "#{indent}"
        put_out "</#{@afk}:presentielijst>"
    end

    def provincie_start attrs
        put_out "\n#{@indent}<#{@afk}:provincie>"
  	put_out "\n#{@indent}<rdf:Seq>"
	put_out "\n#{@indent}  <r:provincienaam rdf:parseType=\"Literal\">#{attrs['naam']}</r:provincienaam>"
    end

    def provincie_end
  	@output.puts "\n#{@indent}</rdf:Seq>"
        indent = "  " * (@level - 1)
  	put_out "#{indent}"
        put_out "</#{@afk}:provincie>"
    end

    def prespersoon_start attrs
        put_out "\n#{@indent}<#{@afk}:prespersoon rdf:parseType=\"Resource\">"
    end

    def prespersoon_end
        put_out "</#{@afk}:prespersoon>"
    end

    def persoon_start attrs
        put_out "\n#{@indent}<#{@afk}:persoon>"
    end

    def persoon_end
        put_out "</#{@afk}:persoon>"
    end

    def noot_start attrs
        put_out "\n#{@indent}<#{@afk}:noot rdf:parseType=\"Literal\">"
    end

    def noot_end
        put_out "</#{@afk}:noot>"
    end

    def resolutie_start attrs
	if !@in_resoluties
            put_out "#{@indent}<#{@afk}:resoluties>"
	    @in_resoluties = true
	    @level += 1
            @indent = "  " * @level
	    put_out "\n#{@indent}<rdf:Seq>"
	    @level += 1
	end
        put_out "\n#{@indent}<#{@afk}:resolutie rdf:parseType=\"Literal\">"
#  	put_out "\n#{@indent}<rdf:Seq>"
    end

    def resolutie_end
#  	@output.puts "\n#{@indent}</rdf:Seq>"
#        indent = "  " * (@level - 1)
#  	@output.puts "\n#{@indent}</rdf:Seq>"
#        indent = "  " * (@level - 1)
  	put_out "#{@indent}"
        put_out "</#{@afk}:resolutie>"
    end

    def p_start attrs
        put_out "<p>"
    end

    def p_end
        put_out "</p>"
    end

    def plaats_start attrs
        put_out "\n#{@indent}<#{@afk}:plaats>"
    end

    def plaats_end
        put_out "</#{@afk}:plaats>"
    end

    def instelling_start attrs
        put_out "\n#{@indent}<#{@afk}:instelling>"
    end

    def instelling_end
        put_out "</#{@afk}:instelling>"
    end

    def bibliografie_start attrs
        put_out "\n#{@indent}<#{@afk}:bibliografie>"
    end

    def bibliografie_end
        put_out "</#{@afk}:bibliografie>"
    end

    def scheepsnaam_start attrs
        put_out "\n#{@indent}<#{@afk}:scheepsnaam>"
    end

    def scheepsnaam_end
        put_out "</#{@afk}:scheepsnaam>"
    end

    def literatuur_start attrs
        put_out "\n#{@indent}<#{@afk}:literatuur>"
    end

    def literatuur_end
        put_out "</#{@afk}:literatuur>"
    end

    def deel_start attrs
        put_out "\n#{@indent}<#{@afk}:deel>"
    end

    def deel_end
        put_out "</#{@afk}:deel>"
    end

    def postprandium_start attrs
	if @in_resoluties
	    @output.puts "\n      </rdf:Seq>"
	    @level -= 1
	    @output.puts "    </#{@afk}:resoluties>"
	    @in_resoluties = false
	end
        put_out "#{@indent}<#{@afk}:postprandium>"
	put_out "\n#{@indent}<rdf:Bag>"
	@in_postprandium = true
    end

    def postprandium_end
#	put_out "</#{@afk}:postprandium>"
    end

    def table
       	{}
    end

    def tag_start(name,attrs)
        if table.has_key? name
            name = table[name][@level] if table[name].has_key?(@level)
        end
        if table.has_key? name
            name = table[name][0] if table[name][1]==@level
        end
        if @level==1
#            code = "#{name[0].upcase}#{@number}"
	    number = sprintf("%s%s%s",attrs['jaar'],attrs['maand'],attrs['dag'])
            code = sprintf("%s%s",name[0].upcase,number)
        lines =<<EOF


  <rdf:Description rdf:about="https://resource.huygens.knaw.nl/ingforms/#{@collection}/#{name}/#{code}">
    <rdf:type rdf:resource="https://resource.huygens.knaw.nl/ingforms/#{@collection}/#{name}" />
EOF
            put_out lines
        else
            begin
                result = self.send( "#{name}_start", attrs )
                rescue => detail
#                    STDERR.puts "#{detail}\nin #{name}"
                end
#            return result
        end
        @level += 1
        @indent = "  " * @level
    end

    def text( text )
        unless text.strip.empty?
	    text.gsub!(/&nbsp;/,"&#160;")
	    text.gsub!(/(\s)&(\s)/,"\\1&amp;\\2")
	    text.gsub!(/([a-zA-Z])&([a-zA-Z])/,"\\1&amp;\\2")
	    text.gsub!(/<br ([^>]*)>/,"<br \\1/>")
	    text.gsub!("//>","/>")
            put_out "#{text.strip}"
#            @text << text
        end
    end

    def tag_end(name)
        if table.has_key? name
            name = table[name][@level-1] if table[name].has_key?(@level-1)
        end
        if (name.eql?("zittingsdag") || name.eql?("postprandium"))
	    if @in_resoluties
		@output.puts "\n      </rdf:Seq>"
		@level -= 1
		@output.puts "    </#{@afk}:resoluties>"
		@in_resoluties = false
	    end
	    if name.eql?("postprandium")
		@output.puts "\n    </rdf:Bag>"
		@output.puts "    </#{@afk}:postprandium>"
		@in_postprandium = false
	    end
            @output.puts "\n  </rdf:Description>" if name.eql?("zittingsdag")
        else
            begin
                result = self.send( "#{name}_end" )
                rescue => detail
                    STDERR.puts "end: #{detail}\nin #{name}"
		    exit(1)
                end
#            return result
        end
        @level -= 1
        @indent = "  " * @level
    end

    def put_out( arg )
        @output.write arg
        arg
    end

end

def help_message
    STDERR.puts "use: ruby parser -d directory -c collection -o output"
    exit(0)
end

if __FILE__ == $0

    inputfile = ""
    directory = ""
    outputfile = ""
    collection = ""
    # evt aanpassen:
    resource = "https://resource.huygens.knaw.nl/ingforms/const_comm"

    (0..(ARGV.size-1)).each do |i|
        case ARGV[i]
            # voeg start en stop tags toe
            when '-i' then begin inputfile = ARGV[i+1] end
            when '-d' then begin directory = ARGV[i+1] end
            when '-c' then begin collection = ARGV[i+1] end
            when '-o' then begin outputfile = ARGV[i+1] end
            when '-r' then begin resource = ARGV[i+1] end
            when '-h' then begin help_message end
        end
    end

    if directory.empty? || outputfile.empty? || collection.empty?
        help_message
    end

    afk = collection[0]
    output = File.new(outputfile,"w")
    # aanpassen:
    rdf_rdf =<<EOF
<?xml version="1.0"?>
<rdf:RDF
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:#{afk}="https://resource.huygens.knaw.nl/#{collection}/#{afk}"
    xmlns:fc="https://resource.huygens.knaw.nl/constitutionele_commissies/fc"
    xmlns:person="https://resource.huygens.knaw.nl/constitutionele_commissies/person">
EOF

    output.puts rdf_rdf

    if File.directory?(directory)
        number = 1
        wd = Dir.getwd
        Dir.chdir(directory)
        file_list = Dir.glob("**/*.xml")
        file_list.each do |filename|
	if !File.directory?(filename)
		Parser.parseFile(filename,output,collection,afk,number)
		number += 1
	    end
        end

    end
    
    rdf_rdf =<<EOF

</rdf:RDF>

EOF

    output.puts rdf_rdf
    
end

