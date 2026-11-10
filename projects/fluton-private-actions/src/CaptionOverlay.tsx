import React from 'react';
import {useCurrentFrame} from 'remotion';
import {film,getSceneAtFrame} from './timeline';
// Orchestrator-owned planning captions. Replace with recording-aligned timings later.
export const CaptionOverlay:React.FC=()=>{
 const frame=useCurrentFrame(),scene=getSceneAtFrame(frame);
 return <svg width="1920" height="1080" viewBox="0 0 1920 1080" style={{position:'absolute',inset:0,pointerEvents:'none'}}>
  {scene.captionLines.map((line,i)=><text key={i} x="960" y={film.safeAreas.captionTop+32+i*film.safeAreas.captionLineHeight} textAnchor="middle" fontSize="32" fontWeight="600" fill={scene.foreground}>{line}</text>)}
  {scene.id==='brand'&&<text x="960" y={film.safeAreas.finalNoticeTop+28} textAnchor="middle" fontSize="28" fontWeight="600" fill={scene.foreground}>{film.finalNotice}</text>}
 </svg>;
};
