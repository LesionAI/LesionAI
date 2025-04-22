import streamlit_authenticator as stauth

# Mot de passe à hacher
passwords = ['test']  

# Hachage
hashed_passwords = stauth.Hasher(passwords).generate()

# Affiche le mot de passe haché
print(hashed_passwords[0])

