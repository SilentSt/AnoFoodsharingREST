import pdfplumber


def text_between(data: str, before: str, after: str):
    start = data.find(before)
    end = data.find(after)
    d = data[start + len(before): end]
    d_ls = d.lstrip()
    d_result = d_ls.replace('  ', ' ')
    return d_result


def get_data_donor_name_org(data: str):
    element1 = '. \n'
    element2 = ', именуем'
    result = text_between(data=data, before=element1, after=element2)
    return {"org_name": result}


def get_data_donor_fullname(data: str):
    start_element = 'в  лице '
    end_element = ',  действ'
    result = text_between(data=data, before=start_element, after=end_element)
    return {"org_representative": result}


def get_data_volunteer_products_count(data: str):
    start_element = 'в количестве'
    end_element = 'единиц.'
    result = text_between(data=data, before=start_element, after=end_element)
    return {"count_products": int(result)}


def get_data_volunteer_name(data: str):
    start_element = 'Жертвователь  Одаряемый'
    end_element = '(подпись)  (Ф.И.О.)  (подпись)  (Ф.И.О.)'
    result = text_between(data=data, before=start_element, after=end_element)
    result_list = [i for i in result.split('\n')]
    phone_recipient = result_list[0].split(":")[0]
    phone_formatted = phone_recipient.replace('Тел. ', '')

    last_name_recipient = result_list[1].split()[1].split('/')[1]
    initials_recipient = result_list[2].split()[1]
    last_name_donor = result_list[1].split()[0].split('/')[1]
    initials_donor = result_list[2].split()[0]

    return {
        "recipient": {"phone": phone_formatted, "full_name": f"{last_name_recipient} {initials_recipient}"},
        "donor": {"full_name": f"{last_name_donor} {initials_donor}"},
    }


def get_elements(data: str):
    start = 'товара'
    end = '2. Вышеуказанные'
    prepare_data = text_between(data=data, before=start, after=end)
    list_elements = prepare_data.split("\n")
    list_without_space = [i.split() for i in list_elements]

    result_data = {"products": []}
    for element in list_without_space:

        if len(element) > 2:
            if element[1] and element[2]:
                element_dict = {
                    "id": int(element[0]),
                    "name": element[1],
                    "count": float(element[2]),
                    "price": float(element[3]),
                    "shelf_life": element[4],
                    "description": element[5]
                }
                result_data["products"].append(element_dict)
        elif len(element) == 2:
            result_data["count_price"] = sum([elem['price'] for elem in result_data["products"]])
            result_data["count_elements"] = sum([elem['count'] for elem in result_data["products"]])
    return result_data


def prepare_pdf(file_path) -> str:
    with pdfplumber.open(file_path) as pdf:
        first_page = pdf.pages[0]
        text = first_page.extract_text()

        reformat_string = ""

        for symbol in text:
            if symbol not in ('_', '\n\n'):
                reformat_string += symbol

        return reformat_string


def shop_parse_pdf(path):
    pdf_str = prepare_pdf(path)
    elements = get_elements(pdf_str)
    donor_name_org = get_data_donor_name_org(pdf_str)
    donor_fullname = get_data_donor_fullname(pdf_str)

    return {**elements, **donor_name_org, **donor_fullname}


def user_parse_pdf(path):
    pdf_str = prepare_pdf(path)
    user_products_count = get_data_volunteer_products_count(pdf_str)
    volunteer_name = get_data_volunteer_name(pdf_str)

    return {**user_products_count, **volunteer_name}