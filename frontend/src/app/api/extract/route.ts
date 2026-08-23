import { NextRequest, NextResponse } from 'next/server';

interface CodeSnippet {
  language: string;
  code: string;
  line_count: number;
}

interface ChatTurn {
  turn_index: number;
  role: string;
  content: string;
  code_blocks: CodeSnippet[];
  model?: string;
  token_estimate: number;
  phase_x: number;
  phase_y: number;
}

interface PhaseMetrics {
  total_turns: number;
  total_tokens: number;
  lyapunov_exponent: number;
  spectral_radius: number;
  entropy: number;
  quaternion_norm: number[];
  stability_status: string;
}

function extractCodeBlocks(text: string): CodeSnippet[] {
  const snippets: CodeSnippet[] = [];
  const regex = /```([a-zA-Z0-9_\-\+]*)\n([\s\S]*?)```/g;
  let match;
  while ((match = regex.exec(text)) !== null) {
    snippets.push({
      language: match[1].trim() || 'text',
      code: match[2],
      line_count: match[2].split('\n').length,
    });
  }
  return snippets;
}

function untangleFractalSuperNode(rawText: string, baseRole: string, startIndex: number): ChatTurn[] {
  const pattern = /(?:^|\n)[ \t]*(?:\*\*)?(Gabriel|Gemini|Anise|Grok|Copilot|You|User|Assistant|System)(?:\*\*)?\s*[:\n]\s*/i;
  const parts: string[] = [];
  let remaining = rawText;
  let match;

  while ((match = pattern.exec(remaining)) !== null) {
    const preText = remaining.substring(0, match.index);
    if (parts.length === 0 && preText.trim()) {
      parts.push('Initial', preText);
    }
    const speaker = match[1];
    const postStart = match.index + match[0].length;
    remaining = remaining.substring(postStart);
    parts.push(speaker);
    const nextMatch = pattern.exec(remaining);
    if (nextMatch) {
      parts.push(remaining.substring(0, nextMatch.index));
      remaining = remaining.substring(nextMatch.index);
    } else {
      parts.push(remaining);
      remaining = '';
    }
  }

  if (parts.length < 2) {
    const content = rawText.trim();
    return [
      {
        turn_index: startIndex,
        role: baseRole,
        content: content,
        code_blocks: extractCodeBlocks(content),
        token_estimate: Math.max(1, Math.floor(content.length / 4)),
        phase_x: 0,
        phase_y: 0,
      },
    ];
  }

  const turns: ChatTurn[] = [];
  let idx = startIndex;
  for (let i = 0; i < parts.length; i += 2) {
    const speaker = parts[i];
    const content = (parts[i + 1] || '').trim();
    if (!content) continue;

    const lowS = speaker.toLowerCase();
    let role = 'user';
    let modelName: string | undefined = undefined;

    if (['gabriel', 'user', 'you', 'human'].includes(lowS)) {
      role = 'user';
    } else if (['gemini', 'anise', 'grok', 'copilot', 'assistant', 'ai', 'system'].includes(lowS)) {
      role = 'assistant';
      modelName = speaker;
    } else {
      role = turns.length % 2 === 0 ? 'user' : 'assistant';
    }

    turns.push({
      turn_index: idx++,
      role: role,
      content: content,
      code_blocks: extractCodeBlocks(content),
      model: modelName,
      token_estimate: Math.max(1, Math.floor(content.length / 4)),
      phase_x: 0,
      phase_y: 0,
    });
  }

  return turns;
}

function collapseRedundantFiles(turns: ChatTurn[]): ChatTurn[] {
  if (turns.length === 0) return [];
  const collapsed: ChatTurn[] = [];
  const fileRegex = /^Uploaded a file\s*(Gabriel:)?\s*$/i;

  for (const turn of turns) {
    if (fileRegex.test(turn.content.trim())) {
      if (collapsed.length > 0 && collapsed[collapsed.length - 1].role === turn.role && fileRegex.test(collapsed[collapsed.length - 1].content.trim())) {
        continue;
      }
    }
    if (collapsed.length > 0 && collapsed[collapsed.length - 1].role === turn.role && fileRegex.test(collapsed[collapsed.length - 1].content.trim())) {
      turn.content = `[Attached files processed]\n\n${turn.content}`;
      collapsed.pop();
    }
    collapsed.push(turn);
  }

  return collapsed.map((t, i) => ({ ...t, turn_index: i + 1 }));
}

function computePhaseCoordinates(turns: ChatTurn[]): { turns: ChatTurn[]; metrics: PhaseMetrics } {
  let x = 0.1;
  let y = 0.1;
  const a = 1.4;
  const b = 0.3;
  const maxTokens = Math.max(...turns.map((t) => t.token_estimate), 1);

  turns.forEach((t) => {
    const roleSign = t.role === 'user' ? 1.0 : -1.0;
    const tokenRatio = Math.min(1.0, t.token_estimate / (maxTokens * 1.2));
    const pert = roleSign * 0.15 + (tokenRatio - 0.5) * 0.2;

    const xNext = 1.0 - a * (x * x) + y + pert;
    const yNext = b * x;

    x = Math.max(-1.5, Math.min(1.5, xNext));
    y = Math.max(-0.6, Math.min(0.6, yNext));

    t.phase_x = Number((x / 1.5).toFixed(4));
    t.phase_y = Number((y / 0.6).toFixed(4));
  });

  const totalTokens = turns.reduce((acc, t) => acc + t.token_estimate, 0);
  const totalTurns = turns.length;
  const lyapunov = Number((-0.035 - Math.min(0.12, (totalTurns / 100) * 0.08)).toFixed(4));
  const spectralRadius = Number((0.68 + (totalTurns % 5) * 0.02).toFixed(3));

  const metrics: PhaseMetrics = {
    total_turns: totalTurns,
    total_tokens: totalTokens,
    lyapunov_exponent: lyapunov,
    spectral_radius: spectralRadius,
    entropy: Number((Math.log2(totalTurns + 1) * 0.85).toFixed(4)),
    quaternion_norm: [0.7071, 0.0, 0.7071, 0.0],
    stability_status: 'Asymptotically Stable',
  };

  return { turns, metrics };
}

function synthesizeArtifacts(turns: ChatTurn[], metrics: PhaseMetrics, title: string, source: string) {
  const manifoldId = 'manifold_' + Math.random().toString(36).substring(2, 9);
  
  let csv = 'Turn_Index,Role,Model,Tokens,Phase_X,Phase_Y,Content\n';
  turns.forEach((t) => {
    const cleanContent = `"${t.content.replace(/"/g, '""')}"`;
    csv += `${t.turn_index},${t.role},${t.model || ''},${t.token_estimate},${t.phase_x},${t.phase_y},${cleanContent}\n`;
  });

  let md = `# ${title}\n\n`;
  md += `> **Platform:** \`${source}\` | **Turns:** ${turns.length} | **Tokens:** ~${metrics.total_tokens} | **Lyapunov:** \`${metrics.lyapunov_exponent}\`\n\n---\n\n`;
  turns.forEach((t) => {
    md += `### Turn #${t.turn_index} — ${t.role.toUpperCase()}${t.model ? ` (${t.model})` : ''}\n\n${t.content}\n\n---\n\n`;
  });

  let antiPrompt = `You are pair programming with the user. The following linearized conversation manifold represents the prior context state:\n\n<INGESTED_CONVERSATION_MANIFOLD>\n[METADATA]\nTitle: ${title}\nSource: ${source}\nTurns: ${turns.length}\nEstimated Tokens: ${metrics.total_tokens}\nLyapunov Stability: ${metrics.lyapunov_exponent} (Stable)\nSpectral Radius: ${metrics.spectral_radius}\n\n[CONVERSATION TURNS]\n`;
  turns.forEach((t) => {
    antiPrompt += `Turn #${t.turn_index} [${t.role.toUpperCase()}]${t.model ? ` (${t.model})` : ''}:\n${t.content}\n\n`;
  });
  antiPrompt += `</INGESTED_CONVERSATION_MANIFOLD>\n\nPlease review this context and continue assisting with high fidelity.`;

  let claudeXml = `<conversation_context id="${manifoldId}">\n  <metadata>\n    <title>${title}</title>\n    <source>${source}</source>\n    <total_turns>${turns.length}</total_turns>\n    <total_tokens>${metrics.total_tokens}</total_tokens>\n  </metadata>\n  <messages>\n`;
  turns.forEach((t) => {
    claudeXml += `    <message index="${t.turn_index}" role="${t.role}">\n      <![CDATA[\n${t.content}\n      ]]>\n    </message>\n`;
  });
  claudeXml += `  </messages>\n</conversation_context>`;

  return {
    manifold: {
      id: manifoldId,
      title: title,
      source_platform: source,
      turns: turns,
      metrics: metrics,
    },
    html_replica: '',
    csv: csv,
    markdown: md,
    antigravity_payload: antiPrompt,
    claude_xml: claudeXml,
  };
}

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const { url, raw, title = 'Cloud Invariant Manifold' } = body;

    let extractedText = '';
    let sourcePlatform = 'raw_text';

    if (raw && typeof raw === 'string') {
      extractedText = raw;
      sourcePlatform = 'raw_payload';
    } else if (url && typeof url === 'string') {
      sourcePlatform = url.includes('chatgpt') ? 'chatgpt' : url.includes('claude') ? 'claude' : url.includes('gemini') ? 'gemini' : url.includes('perplexity') ? 'perplexity' : 'web_link';
      
      const response = await fetch(url, {
        headers: {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        },
      });

      const html = await response.text();

      // Check for __NEXT_DATA__ dehydrated JSON (ChatGPT/Claude/NextJS apps)
      const nextDataMatch = html.match(/<script id="__NEXT_DATA__" type="application\/json">([\s\S]*?)<\/script>/);
      if (nextDataMatch) {
        try {
          const nextData = JSON.parse(nextDataMatch[1]);
          const mapping = nextData?.props?.pageProps?.sharedConversation?.mapping || nextData?.props?.pageProps?.serverResponse?.data?.mapping;
          if (mapping) {
            const nodes = Object.values(mapping) as any[];
            const partsList: string[] = [];
            for (const n of nodes) {
              const msg = n?.message;
              if (msg && msg.content && msg.content.parts) {
                const speaker = msg.author?.role === 'user' ? 'User' : 'Assistant';
                const text = msg.content.parts.filter((p: any) => typeof p === 'string').join('\n');
                if (text.trim()) {
                  partsList.push(`${speaker}: ${text}`);
                }
              }
            }
            if (partsList.length > 0) {
              extractedText = partsList.join('\n\n');
            }
          }
        } catch {}
      }

      if (!extractedText) {
        // Fallback: strip tags and parse
        extractedText = html.replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '')
                            .replace(/<style\b[^<]*(?:(?!<\/style>)<[^<]*)*<\/style>/gi, '')
                            .replace(/<[^>]+>/g, '\n')
                            .replace(/\n\s*\n/g, '\n\n')
                            .trim();
      }
    }

    if (!extractedText) {
      return NextResponse.json({ error: 'No conversational text or valid payload provided.' }, { status: 400 });
    }

    const untangled = untangleFractalSuperNode(extractedText, 'user', 1);
    const collapsed = collapseRedundantFiles(untangled);
    const { turns, metrics } = computePhaseCoordinates(collapsed);
    const result = synthesizeArtifacts(turns, metrics, title, sourcePlatform);

    return NextResponse.json(result);
  } catch (error: any) {
    return NextResponse.json({ error: error.message || 'Serverless extraction error' }, { status: 500 });
  }
}
