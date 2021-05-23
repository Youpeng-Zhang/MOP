import pickle,os,sys,getopt,openpyxl

path=''
input_file=''
output_file=''
change=False

def Parameters():
    print('#########################Parameters#########################'+'\n'+
          '-h           show help information'+'\n'+
          '-c change    input this parameter if you use CHANGE-Seq data'+'\n'+
          '-p           specify the path to the location of the folder "MOP"'+'\n'+
          '-i           specify the input file'+'\n'+
          '-o           specify the output file'+'\n'+
          '############################################################')

try:
    opts,args=getopt.getopt(sys.argv[1:],'h:p:i:o:c:')
    for parameter,value in opts:
        if parameter in ('-h'):
            Parameters()
            sys.exit(1)
        if parameter in ('-c'):
            change=True
        if parameter in ('-p'):
            path=value
        if parameter in ('-i'):
            input_file=value
        if parameter in ('-o'):
            output_file=value
except getopt.GetoptError:
    Parameters()
    sys.exit(1)

if '' not in [path,input_file,output_file]:
    PWM_file=openpyxl.load_workbook(path+'/MOP/model_files/PWM_Multiple_Methods.xlsx').active['A2':'U17']
    PWM_dict={}
    for line in PWM_file:
        key=line[0].value
        value=[]
        for score in line[1:]:
            value.append(score.value)
        PWM_dict[key]=value
    input = open(path+'/MOP/model_files/model_multiple.pkl', 'rb')
    model = pickle.load(input)
    input.close()
    if change is True:
        PWM_file=openpyxl.load_workbook(path+'/MOP/model_files/PWM_CHANGE-Seq.xlsx').active['A2':'U17']
        PWM_dict={}
        for line in PWM_file:
            key=line[0].value
            value=[]
            for score in line[1:]:
                value.append(score.value)
            PWM_dict[key]=value
        input=open(path+'/MOP/model_files/model_change.pkl','rb')
        model=pickle.load(input)
        input.close()

    os.system('echo Reading input file ...')
    IDs=[]
    list_seq_target=[]
    test_x=[]
    for line in open(input_file):
        if line[0]=='>':
            id = line[:-1].split('\t')[0]
            IDs.append(id)
        if line[0]!='>':
            seq_target=line[:-1].split('\t')
            seq=seq_target[0][2:-3]+seq_target[0][-2:]
            target=seq_target[1][2:-3]+seq_target[1][-2:]
            list_seq_target.append(seq_target[0]+'\t'+seq_target[1])
            List = []
            for pos_NA in range(0, len(seq)):
                List.append(float(PWM_dict[seq[pos_NA] + ',' + target[pos_NA]][pos_NA]))
            test_x.append(List)
    scores = model.predict(test_x)
    save_file = open(output_file, 'w')
    os.system('echo Writing to the output file ...')
    save_file.write('#score>0.5 represents off-target' + '\n' + 'ID' + '\t' + 'sgRNA' + '\t' + 'target' + '\t' + 'score' + '\t' + 'class' + '\n')
    index = 0
    for score in scores:
        classification = 'non-off-target'
        if float(score) > 0.5:
            classification = 'off-target'
        save_file.write(IDs[index] + '\t' + list_seq_target[index] + '\t' + '%.3f' % (score) + '\t' + classification + '\n')
        index += 1
    save_file.close()
    os.system('echo Prediction finished!')

else:
    os.system('echo Required parameters are not specified! You can check by parameter -h.')

