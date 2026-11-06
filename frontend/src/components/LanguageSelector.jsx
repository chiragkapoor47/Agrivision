import React, { useState, useRef, useEffect } from 'react';
import { useLanguage } from '../context/LanguageContext';
import { Globe, ChevronDown, Check } from 'lucide-react';

const languages = [
  { code: 'en', name: 'English', native: 'English' },
  { code: 'hi', name: 'Hindi', native: 'हिन्दी' },
  { code: 'as', name: 'Assamese', native: 'অসমীয়া' }
];

export default function LanguageSelector() {
  const { language, setLanguage } = useLanguage();
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef(null);

  const currentLang = languages.find(l => l.code === language) || languages[0];

  useEffect(() => {
    function handleClickOutside(event) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  return (
    <div className="relative inline-block text-left" ref={dropdownRef}>
      <button
        type="button"
        onClick={() => setIsOpen(!isOpen)}
        className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-emerald-800/60 hover:bg-emerald-800 border border-emerald-600/40 text-emerald-100 text-xs sm:text-sm font-medium transition-all shadow-xs"
        aria-expanded={isOpen}
      >
        <Globe className="w-3.5 h-3.5 text-emerald-300" />
        <span>{currentLang.native}</span>
        <ChevronDown className={`w-3 h-3 text-emerald-300 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-44 rounded-xl bg-white shadow-xl ring-1 ring-black/5 py-1 z-50 divide-y divide-gray-100 animate-in fade-in zoom-in-95 duration-100">
          <div className="px-3 py-1.5 text-xs font-semibold text-gray-500 uppercase tracking-wider">
            Select Language
          </div>
          <div className="py-1">
            {languages.map((item) => (
              <button
                key={item.code}
                onClick={() => {
                  setLanguage(item.code);
                  setIsOpen(false);
                }}
                className={`w-full text-left px-3.5 py-2 text-sm flex items-center justify-between hover:bg-emerald-50 transition-colors ${
                  language === item.code ? 'text-emerald-700 font-semibold bg-emerald-50/60' : 'text-gray-700'
                }`}
              >
                <div>
                  <span className="block font-medium">{item.native}</span>
                  <span className="block text-xs text-gray-400">{item.name}</span>
                </div>
                {language === item.code && <Check className="w-4 h-4 text-emerald-600" />}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
