import React, { useRef, useState, useEffect } from 'react';
import { Camera, RefreshCw, Check, X, AlertCircle } from 'lucide-react';

export default function CameraCapture({ onPhotoCaptured, onClose }) {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [stream, setStream] = useState(null);
  const [capturedImage, setCapturedImage] = useState(null);
  const [cameraError, setCameraError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let activeStream = null;

    async function startCamera() {
      try {
        setLoading(true);
        setCameraError(null);
        // Request rear camera on mobile devices with HD resolution
        const constraints = {
          video: {
            facingMode: { ideal: 'environment' },
            width: { ideal: 1280 },
            height: { ideal: 720 }
          },
          audio: false
        };

        const mediaStream = await navigator.mediaDevices.getUserMedia(constraints);
        activeStream = mediaStream;
        setStream(mediaStream);
        if (videoRef.current) {
          videoRef.current.srcObject = mediaStream;
        }
        setLoading(false);
      } catch (err) {
        console.error('Camera access error:', err);
        setCameraError('Unable to access device camera. Please check camera permissions in browser settings or upload a picture from gallery.');
        setLoading(false);
      }
    }

    startCamera();

    return () => {
      if (activeStream) {
        activeStream.getTracks().forEach(track => track.stop());
      }
    };
  }, []);

  const takeSnapshot = () => {
    if (!videoRef.current || !canvasRef.current) return;
    const video = videoRef.current;
    const canvas = canvasRef.current;

    canvas.width = video.videoWidth || 640;
    canvas.height = video.videoHeight || 480;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    const dataUrl = canvas.toDataURL('image/jpeg', 0.92);
    setCapturedImage(dataUrl);
  };

  const retakeSnapshot = () => {
    setCapturedImage(null);
  };

  const confirmPhoto = () => {
    if (!canvasRef.current) return;
    canvasRef.current.toBlob((blob) => {
      if (blob) {
        const file = new File([blob], `leaf_camera_${Date.now()}.jpg`, { type: 'image/jpeg' });
        onPhotoCaptured(file, capturedImage);
      }
    }, 'image/jpeg', 0.92);
  };

  return (
    <div className="bg-stone-900 rounded-2xl overflow-hidden shadow-2xl border border-stone-800 text-white p-4">
      <div className="flex items-center justify-between pb-3 border-b border-stone-800 mb-3">
        <div className="flex items-center gap-2">
          <Camera className="w-5 h-5 text-emerald-400" />
          <h3 className="font-semibold text-stone-100">Smartphone Leaf Camera</h3>
        </div>
        {onClose && (
          <button
            onClick={onClose}
            className="p-1 rounded-full hover:bg-stone-800 text-stone-400 hover:text-white transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        )}
      </div>

      {cameraError ? (
        <div className="py-8 px-4 text-center">
          <AlertCircle className="w-12 h-12 text-amber-400 mx-auto mb-3" />
          <p className="text-stone-300 text-sm max-w-sm mx-auto mb-4">{cameraError}</p>
          <button
            onClick={onClose}
            className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 rounded-xl text-sm font-medium transition-colors"
          >
            Switch to File Upload
          </button>
        </div>
      ) : (
        <div className="relative">
          <div className="relative aspect-4/3 w-full bg-black rounded-xl overflow-hidden flex items-center justify-center">
            {loading && (
              <div className="absolute inset-0 flex items-center justify-center bg-stone-900/80 z-10">
                <RefreshCw className="w-8 h-8 text-emerald-400 animate-spin" />
              </div>
            )}

            {capturedImage ? (
              <img
                src={capturedImage}
                alt="Captured leaf preview"
                className="w-full h-full object-contain"
              />
            ) : (
              <>
                <video
                  ref={videoRef}
                  autoPlay
                  playsInline
                  muted
                  className="w-full h-full object-cover"
                />
                {/* Visual reticle targeting guide for farmers */}
                <div className="absolute inset-8 border-2 border-dashed border-emerald-400/60 rounded-3xl pointer-events-none flex items-center justify-center">
                  <span className="bg-stone-900/60 backdrop-blur-xs text-emerald-200 text-xs px-3 py-1 rounded-full font-medium">
                    Center diseased leaf inside frame
                  </span>
                </div>
              </>
            )}
          </div>

          {/* Hidden canvas for snapshot rendering */}
          <canvas ref={canvasRef} className="hidden" />

          {/* Camera controls */}
          <div className="mt-4 flex items-center justify-center gap-4">
            {capturedImage ? (
              <>
                <button
                  type="button"
                  onClick={retakeSnapshot}
                  className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-stone-800 hover:bg-stone-700 text-stone-200 text-sm font-medium transition-colors"
                >
                  <RefreshCw className="w-4 h-4" />
                  Retake Photo
                </button>
                <button
                  type="button"
                  onClick={confirmPhoto}
                  className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-sm font-semibold transition-colors shadow-lg shadow-emerald-900/30"
                >
                  <Check className="w-4 h-4" />
                  Use This Leaf Image
                </button>
              </>
            ) : (
              <button
                type="button"
                onClick={takeSnapshot}
                disabled={loading}
                className="inline-flex items-center gap-2 px-6 py-3 rounded-full bg-emerald-500 hover:bg-emerald-400 text-stone-950 font-bold transition-transform active:scale-95 shadow-lg shadow-emerald-500/25"
              >
                <Camera className="w-5 h-5 text-stone-950" />
                Capture Leaf Photo
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
