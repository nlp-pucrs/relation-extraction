def generate_input(xml_nerp):
	with open('input_file.txt', 'w+') as output_file:
		with open(xml_nerp) as xml:
			doc = False
			em = False
			org = False
			pes = False
			text = []
			annotated_text = []
			for line in xml:
				if line.find('<DOC DOCID=') != -1:
					doc = True
					continue
				if line.find('</DOC>') != -1:
					doc = False
					for word in text:
						if word.find('<EM') != -1:
							em = True
							continue
						if word.find('</EM>') != -1:
								em = False
						if em == True:
							if word.find('ID=') != -1:
								continue
							if word.find('CATEG=') != -1:
								if word.find('"ORGANIZACAO"') != -1:
									annotated_text.append([word[word.find('>')+1:], 'ORG'])
								elif word.find('"PESSOA"') != -1:
									annotated_text.append([word[word.find('>')+1:], 'PER'])
								elif word.find('"LOCAL"') != -1:
									annotated_text.append([word[word.find('>')+1:], 'PLC'])
								else:
									annotated_text.append([word[word.find('>')+1:], 'X'])
									em = False
							else:
								annotated_text.append([word, 'I'])
							continue
						if word.find('</EM>') != -1:
							if word == '</EM>':
								continue
							word = word.replace('</EM>', '')
						annotated_text.append([word, 'X'])

					first_word = True
					curr_id = 0
					curr_entity = None
					entities = []
					for word, tag in annotated_text:
						if first_word:
							frase = word
							first_word = False
						elif tag == 'I':
							frase = frase + '_' + word
						else:
							frase = frase + ' ' + word
						if tag == 'ORG' or tag == 'PER' or tag == 'PLC':
							if tag == 'ORG':
								entity_org = True
							else:
								entity_org = False

							id_entity = curr_id
							curr_entity = word
							tag_entity = tag
						if tag == 'I':
							curr_entity = curr_entity + '_' + word
						if tag == 'X' and curr_entity != None:
							entities.append([curr_entity, id_entity, entity_org, tag_entity])
							curr_entity = None
						curr_id += 1
					for i in range(len(entities)):
						for j in range(i+1, len(entities)):
							if entities[i][2] or entities[j][2]:
								to_write = '\t'.join([frase, str(entities[i][1]), entities[i][0], entities[i][3], str(entities[j][1]), entities[j][0], entities[j][3]])
								output_file.write(to_write + '\n')
					annotated_text = []
					text = []
					
				if doc:
					text.extend(line.split())