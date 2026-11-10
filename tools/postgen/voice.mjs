#!/usr/bin/env node
/**
 * Fetch narration from PostGen for a project and save it into the local project.
 *
 *   POSTGEN_API_KEY=… node tools/postgen/voice.mjs <project-slug> --postgen-project=<uuid> \
 *       [--script=path] [--confirm]
 *
 * Without --confirm it only prints the script + caps and exits: generation is paid.
 */
import fs from 'node:fs';
import path from 'node:path';
import {ROOT,project} from '../lib.mjs';
import {generateVoiceover,listAssets} from './client.mjs';

const [slug,...rest]=process.argv.slice(2);
const opt={};
for(const a of rest){
  const m=/^--([a-z-]+)=?(.*)$/.exec(a);
  if(!m)throw new Error(`Expected --name=value, received ${a}`);
  opt[m[1]]=m[2]||'true';
}
const pgProject=opt['postgen-project'];
if(!slug||!pgProject){console.error('Usage: POSTGEN_API_KEY=… node tools/postgen/voice.mjs <slug> --postgen-project=<uuid> [--script=production/voiceover.txt] [--confirm]');process.exit(1);}
const {dir}=project(slug);
const scriptPath=path.join(dir,opt.script||'production/voiceover.txt');
const text=fs.readFileSync(scriptPath,'utf8').trim();
if(!text)throw new Error('Narration script is empty.');
if(!opt.confirm){
  console.log(`Script (${text.length} chars):\n\n${text}\n\nDry run. Re-run with --confirm to spend 1 ElevenLabs generation (caps apply).`);
  process.exit(0);
}
const out=await generateVoiceover(pgProject,text);
const assets=await listAssets(pgProject);
const asset=(assets.assets||[]).find(a=>a.id===out.asset_id);
if(!asset?.url)throw new Error('Generated asset not found in the project asset list.');
const bytes=Buffer.from(await (await fetch(asset.url)).arrayBuffer());
const dest=path.join(dir,'production','narration.mp3');
fs.mkdirSync(path.dirname(dest),{recursive:true});
fs.writeFileSync(dest,bytes);
fs.writeFileSync(path.join(dir,'production','narration.alignment.json'),JSON.stringify({
  assetId:out.asset_id,voiceId:out.voice_id,characters:out.characters,caps:out.caps,
  alignment:out.alignment,scriptSHA256:undefined
},null,2)+'\n');
fs.writeFileSync(path.join(dir,'production','voiceover.txt'),text+'\n');
console.log(`Saved ${dest} (${bytes.length} bytes). Caps left today: ${out.caps?.remaining_today}.`);
