def recommendations(disease):
    remedies = {
        "COVID": {
            "home": [
                {"name": "Drink warm water with lemon", "image": "lemon_water.png"},
                {"name": "Breathing exercises", "image": "breathing.png"}
            ],
            "medicine": [
                {"name": "Consult doctor", "image": "doctor.png"},
                {"name": "Vitamin C", "image": "vitamin_c.png"}
            ]
        },
        "Flu": {
            "home": [
                {"name": "Drink ginger tea", "image": "ginger_tea.png"},
                {"name": "Take steam inhalation", "image": "flu_remedy.png"}
            ],
            "medicine": [
                {"name": "Paracetamol", "image": "paracetamol.png"},
                {"name": "Cough syrup", "image": "cough_syrup.png"}
            ]
        }
    }

    return remedies.get(disease, {
        "home": [{"name": "No remedies found", "image": "default.png"}],
        "medicine": [{"name": "Consult doctor", "image": "default.png"}]
    })
