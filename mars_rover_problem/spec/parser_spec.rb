describe Parser do
    let(:parser) { Parser.new("sample_data.txt") }
    
    describe '#initialize' do
        it 'should store the input file in a variable' do
            expect(parser.instance_variable_get(:@input)).to eq("sample_data.txt")
        end
        
        it 'should store its formatted output as a hash of arrays' do
            expect(parser.instance_variable_get(:@output)).to eq({
                :upper_bounds => [], 
                :rovers => [],
                :commands => []
            })
        end
        
        it 'should set the next id to 1' do
            expect(parser.instance_variable_get(:@next_id)).to eq(1)
        end
    end
    
    describe '#parse_text' do
        it 'should set the right id for each rover\'s info' do
            parser.parse_text
            expect(parser.instance_variable_get(:@output)[:rovers][0][:id]).to eq(1)
            expect(parser.instance_variable_get(:@next_id)).to eq(3)
        end

        it 'should parse the boundaries and add them to output' do
            expect(parser.parse_text[:upper_bounds]).to eq([5,5])
        end
        
        it 'should parse rovers\' info and add them to output' do
            expect(parser.parse_text[:rovers]).to eq([
                {id: 1, position: [1,2], direction: "N"}, 
                {id: 2, position: [3,3], direction: "E"}
            ])
        end

        it 'should parse commands and add them to output' do
            expect(parser.parse_text[:commands]).to eq([
                {id: 1, orders: ["L", "M", "L", "M", "L", "M", "L", "M", "M"]},
                {id: 2, orders: ["M","M", "R", "M", "M", "R", "M", "R", "R", "M"]}
            ])
        end
    end
end