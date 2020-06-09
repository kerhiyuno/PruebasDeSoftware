import boto3
import datetime

s3 = boto3.client('s3')
response = s3.list_buckets()

print('Buckets existentes:')
for bucket in response['Buckets']:
    print(f'  {bucket["Name"]}')

def estandarizar(detectadas):
    for i in range(len(detectadas)):
        detectadas[i]=detectadas[i].lower()
        detectadas[i]=detectadas[i].replace(" ","")
        detectadas[i]=detectadas[i].replace(".","")
        detectadas[i]=detectadas[i].replace("\\n","")
        detectadas[i]=detectadas[i].replace(",","")
        detectadas[i]=detectadas[i].replace("[","")
        detectadas[i]=detectadas[i].replace("]","")
        detectadas[i]=detectadas[i].replace("¿","")
        detectadas[i]=detectadas[i].replace("?","")
        detectadas[i]=detectadas[i].replace("!","")
        detectadas[i]=detectadas[i].replace("¡","")
        detectadas[i]=detectadas[i].replace("-","")
        detectadas[i]=detectadas[i].replace("á","a")
        detectadas[i]=detectadas[i].replace("é","e")
        detectadas[i]=detectadas[i].replace("í","i")
        detectadas[i]=detectadas[i].replace("ó","o")
        detectadas[i]=detectadas[i].replace("ú","u")
        detectadas[i]=detectadas[i].replace("Á","A")
        detectadas[i]=detectadas[i].replace("É","E")
        detectadas[i]=detectadas[i].replace("Í","I")
        detectadas[i]=detectadas[i].replace("Ó","O")
        detectadas[i]=detectadas[i].replace("Ú","U")
        detectadas[i]=detectadas[i].replace("@","")
    if ("" in detectadas):
        detectadas.remove('')


def detect_text(photo, bucket):

    client=boto3.client('rekognition')

    response=client.detect_text(Image={'S3Object':{'Bucket':bucket,'Name':photo}})
                        
    textDetections=response['TextDetections']
    print ('Detected text\n----------')
    arreglo=[]
    for text in textDetections:
            if (text['Type']=="WORD" and float(text['Confidence'])>97):
                arreglo.append(text['DetectedText'])
    return arreglo

def main():
    log = open('log.txt', 'a')
    bucket='proyectoimagenesps'
    photo='keep.png'
    detectadas=detect_text(photo,bucket)
    estandarizar(detectadas)
    while True:
        archivo=input("Ingrese nombre de imagen: ")
        detectadas2=detect_text(archivo,bucket)
        estandarizar(detectadas2)
        respuesta=False
        for j in range(len(detectadas2)):
            if (detectadas[0:]==detectadas2[j:(j+len(detectadas[0:]))]):
                respuesta=True
        if (respuesta==True):
            log.write("Hora: "+ datetime.datetime.now().strftime('%H:%M:%S')+"\n")
            log.write("Imagen: "+ archivo+ "\n")
            log.write("Resultado:VERDADERO, SI contiene el texto de "+photo+"\n")
            log.write("\n")
        else:
            log.write("Hora: "+ datetime.datetime.now().strftime('%H:%M:%S')+"\n")
            log.write("Imagen: "+ archivo+ "\n")
            log.write("Resultado:FALSO, NO contiene el texto de "+photo+"\n")
            log.write("\n")
if __name__ == "__main__":
    main()
