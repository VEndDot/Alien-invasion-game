class ReadAndWrite():   
    def read_record_from_file():
        """Выводим рекорд, который нужно побить"""
        # Открываем файл для чтения
        with open('records.txt', 'r') as file:
            # Читаем число из файла
            number = int(file.read())
        return number 
    
    def write_record_to_file(records):
        """Записываем новый рекорд"""
        # Открываем файл для записи
        with open('records.txt', 'w') as file:
            # Записываем число в файл
            file.write(str(records))