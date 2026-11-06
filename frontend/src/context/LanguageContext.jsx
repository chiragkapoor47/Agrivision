import React, { createContext, useContext, useState, useEffect } from 'react';
import en from '../translations/en.json';
import hi from '../translations/hi.json';
import as from '../translations/as.json';

const translations = { en, hi, as };

const LanguageContext = createContext();

export const LanguageProvider = ({ children }) => {
  const [language, setLanguageState] = useState(() => {
    return localStorage.getItem('agri_lang') || 'en';
  });

  const setLanguage = (lang) => {
    if (translations[lang]) {
      setLanguageState(lang);
      localStorage.setItem('agri_lang', lang);
    }
  };

  const t = (path, defaultText = '') => {
    const keys = path.split('.');
    let current = translations[language];
    for (const key of keys) {
      if (current && current[key] !== undefined) {
        current = current[key];
      } else {
        // Fallback to English
        let fallback = translations.en;
        for (const fbKey of keys) {
          if (fallback && fallback[fbKey] !== undefined) {
            fallback = fallback[fbKey];
          } else {
            return defaultText || path;
          }
        }
        return fallback;
      }
    }
    return current !== undefined ? current : (defaultText || path);
  };

  return (
    <LanguageContext.Provider value={{ language, setLanguage, t }}>
      {children}
    </LanguageContext.Provider>
  );
};

export const useLanguage = () => useContext(LanguageContext);
