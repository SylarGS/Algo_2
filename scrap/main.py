from bs4 import BeautifulSoup
import requests
import csv


def scrap_listing(page, brand, year_max, year_min, km_min, km_max, energy, price_max, price_min):
    url = f"https://www.lacentrale.fr/listing?energies={energy}&makesModelsCommercialNames={brand}&mileageMax={km_max}&mileageMin={km_min}&page={page}&priceMax={price_max}&priceMin={price_min}&yearMax={year_max}&yearMin={year_min}"
    reponse = requests.get(url)
    print(url)
    return reponse.text


def lancement():
    brand = input("Brand : ")
    year_max = int(input("Year max : "))
    year_min = int(input("Year min : "))
    km_min = int(input("mileage min : "))
    km_max = int(input("mileage max : "))
    energy = input("Energy : ")
    price_min = int(input("price min : "))
    price_max = int(input("price max : "))
    page = 0
    page_number = ""
    while type(page_number) != int:
        try:
            page_number = int(
                input("Nombre de page que vous souhaitez scrap : "))
        except:
            print("Error : please put a number !")

    # Création d'un fichier csv nommé car.csv
    fd = open("car.csv", "w")
    csv_writer = csv.writer(fd)
    csv_writer.writerow(
        ['brand', 'model', 'year', 'price', 'fuel', 'mileage', 'motor'])

    # Script lancé selon le nombre de page
    while page != page_number:
        html_page = scrap_listing(page, brand, year_max, year_min,
                                  km_min, km_max, energy, price_max, price_min)
        soup = BeautifulSoup(html_page, 'html.parser')
        for result in soup.find_all('div', 'Vehiculecard_Vehiculecard_cardBody'):
            car_name = result.find('h3').get_text()

            cost = soup.find(
                'span', "Text_Text_text Vehiculecard_Vehiculecard_price Text_Text_subtitle2")
            cost2 = cost.get_text()

            year = soup.find_all(
                'div', class_="Text_Text_text Vehiculecard_Vehiculecard_characteristicsItems Text_Text_body2")[0]

            type_fuel = soup.find_all(
                'div', class_="Text_Text_text Vehiculecard_Vehiculecard_characteristicsItems Text_Text_body2")[3]

            motor_name = soup.find(
                'div', class_='Text_Text_text Vehiculecard_Vehiculecard_subTitle Text_Text_body2').get_text()

            mileage_car_brut = soup.find_all(
                'div', class_="Text_Text_text Vehiculecard_Vehiculecard_characteristicsItems Text_Text_body2")[1]
            mileage_car_text = mileage_car_brut.get_text()

            # suppression des espaces et des elements string
            final_cost = cost2.rstrip("€").replace(" ", "")
            mileage_car = mileage_car_text.rstrip("km").replace(" ", "")

            csv_writer.writerow([brand, car_name.lstrip(brand), int(year.get_text()), int(
                final_cost), type_fuel.get_text(), int(mileage_car), motor_name])
            print("Car name : ", car_name)
            print("Year : ", (year.get_text()))
            print("Cost : ", cost.get_text())
            print("Mileage : ", mileage_car_brut.get_text())
        page += 1
    fd.close()


if __name__ == "__main__":
    lancement()
