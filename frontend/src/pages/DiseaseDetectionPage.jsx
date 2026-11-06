import React, { useState, useEffect, useRef } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useLanguage } from '../context/LanguageContext';
import { useAuth } from '../context/AuthContext';
import { predictApi, agriApi } from '../services/api';
import CameraCapture from '../components/CameraCapture';
import { 
  Camera, Upload, Sparkles, RefreshCw, X, AlertCircle, 
  CheckCircle2, ArrowRight, HelpCircle, Layers, ShieldAlert 
} from 'lucide-react';

export default function DiseaseDetectionPage() {
  const { t, language } = useLanguage();
  const { user } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const [activeTab, setActiveTab] = useState('upload'); // 'upload' | 'camera'
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [cropHint, setCropHint] = useState('auto');
  const [cropsList, setCropsList] = useState([]);
  const [isScanning, setIsScanning] = useState(false);
  const [scanStepMessage, setScanStepMessage] = useState('');
  const [errorMessage, setErrorMessage] = useState(null);

  const fileInputRef = useRef(null);

  // Load supported crops list
  useEffect(() => {
    async function loadCrops() {
      try {
        const crops = await agriApi.getCrops();
        setCropsList(crops);
      } catch (e) {
        console.warn('Failed to load crops list:', e);
      }
    }
    loadCrops();
  }, []);

  // Check if routed with sample preset from Landing Page
  useEffect(() => {
    if (location.state?.samplePreset) {
      const preset = location.state.samplePreset;
      // Fetch sample image from server
      fetch(`/uploads/${preset.file}`)
        .then(res => res.blob())
        .then(blob => {
          const file = new File([blob], preset.file, { type: 'image/jpeg' });
          setSelectedFile(file);
          setPreviewUrl(`/uploads/${preset.file}`);
          if (preset.crop && preset.crop !== 'All') {
            setCropHint(preset.crop);
          }
        })
        .catch(err => console.warn('Could not load preset sample:', err));
    }
  }, [location.state]);

  const handleFileSelect = (e) => {
    const file = e.target.files?.[0];
    if (file) {
      processSelectedFile(file);
    }
  };

  const processSelectedFile = (file) => {
    setErrorMessage(null);
    if (!file.type.startsWith('image/')) {
      setErrorMessage('Please select a valid image file (JPG, PNG, or WEBP).');
      return;
    }
    if (file.size > 15 * 1024 * 1024) {
      setErrorMessage('File size exceeds 15MB limit. Please choose a smaller photo.');
      return;
    }

    setSelectedFile(file);
    const objectUrl = URL.createObjectURL(file);
    setPreviewUrl(objectUrl);
  };

  const handleCameraPhoto = (file, dataUrl) => {
    setSelectedFile(file);
    setPreviewUrl(dataUrl);
    setActiveTab('upload'); // return to preview
  };

  const handleDrop = (e) => {
    e.preventDefault();
    if (e.dataTransfer.files?.[0]) {
      processSelectedFile(e.dataTransfer.files[0]);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const clearSelection = () => {
    setSelectedFile(null);
    setPreviewUrl(null);
    setErrorMessage(null);
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  const executeDiagnosticScan = async () => {
    if (!selectedFile) {
      setErrorMessage('Please select or capture a plant leaf image first.');
      return;
    }

    try {
      setIsScanning(true);
      setErrorMessage(null);

      // Multi-phase progress messages for transparency
      setScanStepMessage('Preprocessing leaf image and normalizing color spaces...');
      await new Promise(r => setTimeout(r, 400));

      setScanStepMessage('Running MobileNetV2 neural feature extraction...');
      await new Promise(r => setTimeout(r, 450));

      setScanStepMessage('Quantifying lesion boundaries and calculating severity % via OpenCV...');

      const formData = new FormData();
      formData.append('file', selectedFile);
      if (cropHint && cropHint !== 'auto') {
        formData.append('crop_hint', cropHint);
      }
      formData.append('state', user?.state || 'Assam');
      formData.append('district', user?.district || 'Kamrup');
      formData.append('village', user?.village || 'Azara');
      formData.append('language', language || 'en');

      const result = await predictApi.predictLeaf(formData);

      setScanStepMessage('Compiling certified organic and chemical prescriptions...');
      await new Promise(r => setTimeout(r, 300));

      // Navigate to results page with diagnosis response
      navigate(`/diagnosis/${result.id}`, { state: { diagnosisResult: result } });

    } catch (err) {
      console.error('Scan error:', err);
      setErrorMessage(err.message || 'Diagnosis failed. Please verify that the image contains a clear plant leaf.');
      setIsScanning(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Page Header */}
      <div className="text-center space-y-2">
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 text-xs font-semibold">
          <Sparkles className="w-3.5 h-3.5 text-emerald-600" />
          <span>MobileNetV2 Transfer Learning + OpenCV Severity Engine</span>
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-stone-900 tracking-tight">
          {t('detect.title', 'Plant Leaf Disease Diagnostic Scanner')}
        </h1>
        <p className="text-sm sm:text-base text-stone-600 max-w-2xl mx-auto">
          {t('detect.subtitle', 'Take a clear picture of the diseased leaf or upload an existing image from your smartphone gallery.')}
        </p>
      </div>

      {/* Crop Selector & Parameters */}
      <div className="bg-white p-4 sm:p-5 rounded-2xl border border-emerald-100 shadow-xs flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-4">
        <div className="flex-1">
          <label className="block text-xs font-bold text-stone-700 uppercase tracking-wider mb-1">
            {t('detect.crop_hint_label', 'Select Crop Type (Optional)')}
          </label>
          <select
            value={cropHint}
            onChange={(e) => setCropHint(e.target.value)}
            className="w-full bg-stone-50 border border-stone-200 rounded-xl px-3.5 py-2.5 text-sm font-medium text-stone-900 focus:outline-hidden focus:ring-2 focus:ring-emerald-500 transition-all"
          >
            <option value="auto">🌿 {t('detect.crop_hint_auto', 'Auto-Detect Species (AI Identifies Crop)')}</option>
            {cropsList.map((c) => (
              <option key={c.id} value={c.name}>
                {c.name} {language !== 'en' && `(${c[`name_${language}`] || ''})`}
              </option>
            ))}
          </select>
        </div>

        <div className="text-xs text-stone-500 bg-stone-50 p-3 rounded-xl border border-stone-200/60 max-w-xs">
          <span className="font-semibold text-stone-700 block mb-0.5">Location Customization:</span>
          <span>{user?.district || 'Kamrup'}, {user?.state || 'Assam'}</span>
        </div>
      </div>

      {/* Main Upload / Camera Workspace */}
      <div className="bg-white rounded-3xl border border-emerald-100 shadow-md overflow-hidden">
        {/* Tab switchers */}
        <div className="flex border-b border-gray-100 bg-stone-50/60">
          <button
            type="button"
            onClick={() => setActiveTab('upload')}
            className={`flex-1 py-3.5 text-center text-sm font-semibold flex items-center justify-center gap-2 border-b-2 transition-colors ${
              activeTab === 'upload'
                ? 'border-emerald-600 text-emerald-800 bg-white'
                : 'border-transparent text-stone-500 hover:text-stone-800'
            }`}
          >
            <Upload className="w-4 h-4" />
            <span>{t('detect.upload_tab', 'Upload Image')}</span>
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('camera')}
            className={`flex-1 py-3.5 text-center text-sm font-semibold flex items-center justify-center gap-2 border-b-2 transition-colors ${
              activeTab === 'camera'
                ? 'border-emerald-600 text-emerald-800 bg-white'
                : 'border-transparent text-stone-500 hover:text-stone-800'
            }`}
          >
            <Camera className="w-4 h-4" />
            <span>{t('detect.camera_tab', 'Use Camera')}</span>
          </button>
        </div>

        <div className="p-6 sm:p-8">
          {activeTab === 'camera' ? (
            <CameraCapture
              onPhotoCaptured={handleCameraPhoto}
              onClose={() => setActiveTab('upload')}
            />
          ) : (
            <div>
              {!previewUrl ? (
                /* Empty Upload Dropzone */
                <div
                  onDrop={handleDrop}
                  onDragOver={handleDragOver}
                  onClick={() => fileInputRef.current?.click()}
                  className="border-2 border-dashed border-emerald-300 hover:border-emerald-500 rounded-3xl p-8 sm:p-12 text-center cursor-pointer bg-emerald-50/20 hover:bg-emerald-50/50 transition-all group"
                >
                  <input
                    ref={fileInputRef}
                    type="file"
                    accept="image/*"
                    onChange={handleFileSelect}
                    className="hidden"
                  />
                  <div className="w-16 h-16 rounded-3xl bg-emerald-100 group-hover:bg-emerald-200 text-emerald-700 flex items-center justify-center mx-auto mb-4 transition-colors">
                    <Upload className="w-8 h-8 text-emerald-700" />
                  </div>
                  <h3 className="text-base sm:text-lg font-bold text-stone-900 mb-1">
                    {t('detect.drag_drop', 'Drag and drop leaf image here, or')}
                  </h3>
                  <p className="text-sm font-semibold text-emerald-700 hover:underline mb-2">
                    {t('detect.browse_files', 'Browse from Device')}
                  </p>
                  <p className="text-xs text-stone-500 max-w-sm mx-auto">
                    {t('detect.file_limits', 'Supports JPG, PNG, WEBP up to 15MB. Ensure leaf blade fills frame.')}
                  </p>
                </div>
              ) : (
                /* Preview with Image */
                <div className="space-y-6">
                  <div className="relative aspect-4/3 max-w-md mx-auto rounded-2xl overflow-hidden bg-stone-950 shadow-inner border border-stone-200">
                    <img
                      src={previewUrl}
                      alt="Selected Leaf Preview"
                      className="w-full h-full object-contain"
                    />
                    <button
                      type="button"
                      onClick={clearSelection}
                      className="absolute top-3 right-3 p-1.5 rounded-full bg-stone-900/80 hover:bg-stone-900 text-white transition-colors"
                      title="Remove image"
                    >
                      <X className="w-5 h-5" />
                    </button>
                    <div className="absolute bottom-3 left-3 bg-stone-900/80 backdrop-blur-xs text-emerald-300 text-xs px-3 py-1 rounded-full font-medium">
                      Selected: {selectedFile?.name || 'Captured Leaf'}
                    </div>
                  </div>

                  {/* Action Bar */}
                  <div className="flex flex-col sm:flex-row items-center justify-center gap-3">
                    <button
                      type="button"
                      onClick={clearSelection}
                      disabled={isScanning}
                      className="w-full sm:w-auto px-5 py-3 rounded-xl border border-stone-300 text-stone-700 text-sm font-semibold hover:bg-stone-50 transition-colors"
                    >
                      Choose Different Leaf
                    </button>
                    <button
                      type="button"
                      onClick={executeDiagnosticScan}
                      disabled={isScanning}
                      className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-8 py-3.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-base transition-all shadow-lg shadow-emerald-600/30 active:scale-95 disabled:opacity-50"
                    >
                      {isScanning ? (
                        <>
                          <RefreshCw className="w-5 h-5 animate-spin" />
                          <span>Analyzing Leaf...</span>
                        </>
                      ) : (
                        <>
                          <Sparkles className="w-5 h-5 text-emerald-200" />
                          <span>{t('detect.btn_start_scan', 'Analyze Leaf Disease')}</span>
                          <ArrowRight className="w-5 h-5" />
                        </>
                      )}
                    </button>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Scanning Progress Overlay */}
          {isScanning && (
            <div className="mt-6 p-6 rounded-2xl bg-emerald-950 text-white border border-emerald-800 animate-in fade-in duration-200">
              <div className="flex items-center gap-3 mb-3">
                <RefreshCw className="w-6 h-6 text-emerald-400 animate-spin" />
                <h4 className="font-bold text-base text-emerald-200">
                  {t('detect.scanning_title', 'AI Model Scanning Leaf...')}
                </h4>
              </div>
              <p className="text-xs text-emerald-300/80 mb-3">{scanStepMessage}</p>
              {/* Progress bar animation */}
              <div className="w-full h-2 rounded-full bg-emerald-900 overflow-hidden">
                <div className="h-full bg-emerald-400 rounded-full animate-pulse transition-all" style={{ width: '85%' }}></div>
              </div>
            </div>
          )}

          {/* Error Message */}
          {errorMessage && (
            <div className="mt-4 p-4 rounded-xl bg-red-50 border border-red-200 text-red-800 flex items-start gap-3">
              <AlertCircle className="w-5 h-5 text-red-600 shrink-0 mt-0.5" />
              <div className="text-sm">
                <strong className="block font-semibold">Diagnosis Alert</strong>
                {errorMessage}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
