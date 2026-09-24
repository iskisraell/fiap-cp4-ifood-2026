import pptxgen from 'pptxgenjs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const out = path.join(here, 'CP4_iFood_Apresentacao.pptx');
const pptx = new pptxgen();
pptx.layout = 'LAYOUT_16x9';
pptx.author = 'Grupo Perceptron';
pptx.subject = 'CP4: Case iFood';
pptx.title = 'CP4 | Case iFood';
pptx.lang = 'pt-BR';
pptx.theme = {
  headFontFace: 'Montserrat',
  bodyFontFace: 'Montserrat',
  lang: 'pt-BR',
};
pptx.defineLayout({ name: 'FIAP_WIDE', width: 10, height: 5.625 });
pptx.layout = 'FIAP_WIDE';

const C = {
  bg: '1C1C1C',
  card: '2D2D2D',
  pink: 'ED1165',
  white: 'FFFFFF',
  body: 'E0E0E0',
  secondary: 'C0C0C0',
  muted: '808080',
  grey: '6B7280',
  amber: 'F59E0B',
};
const W = 10;
const H = 5.625;
const FONT = 'Montserrat';

function rect(slide, x, y, w, h, color) {
  slide.addShape(pptx.ShapeType.rect, {
    x, y, w, h,
    fill: { color },
    line: { color, transparency: 100 },
  });
}

function text(slide, value, x, y, w, h, options = {}) {
  slide.addText(value, {
    x, y, w, h,
    fontFace: FONT,
    fontSize: 16,
    color: C.body,
    margin: 0,
    breakLine: false,
    valign: 'mid',
    fit: 'shrink',
    ...options,
  });
}

function base(title, kicker, page) {
  const slide = pptx.addSlide();
  slide.background = { color: C.bg };
  text(slide, kicker.toUpperCase(), 0.55, 0.32, 8.9, 0.22, {
    fontSize: 10,
    bold: true,
    charSpacing: 2.2,
    color: C.pink,
  });
  text(slide, title, 0.55, 0.72, 8.95, 0.7, {
    fontSize: 31,
    bold: true,
    color: C.white,
    valign: 'mid',
  });
  text(slide, 'PERCEPTRON  |  CP4 · CASE IFOOD', 0.55, 5.22, 7.5, 0.18, {
    fontSize: 9,
    color: C.muted,
    charSpacing: 1.2,
  });
  text(slide, String(page).padStart(2, '0'), 9.12, 5.18, 0.32, 0.22, {
    fontSize: 10,
    color: C.secondary,
    align: 'right',
  });
  return slide;
}

function card(slide, x, y, w, h, title, body, accent = C.pink) {
  rect(slide, x, y, w, h, C.card);
  rect(slide, x, y, 0.06, h, accent);
  text(slide, title, x + 0.22, y + 0.18, w - 0.42, 0.3, {
    fontSize: 16,
    bold: true,
    color: C.white,
  });
  text(slide, body, x + 0.22, y + 0.59, w - 0.42, h - 0.75, {
    fontSize: 12,
    color: C.body,
    valign: 'top',
    breakLine: false,
  });
}

// 1. A pergunta de negócio abre a história.
{
  const slide = pptx.addSlide();
  slide.background = { color: C.bg };
  rect(slide, 0, 0, 0.12, H, C.pink);
  text(slide, 'COGNITIVE DATA SCIENCE  +  MACHINE LEARNING & MODELLING', 0.65, 0.55, 8.7, 0.25, {
    fontSize: 10,
    bold: true,
    charSpacing: 1.7,
    color: C.secondary,
  });
  text(slide, 'CP4 | CASE IFOOD', 0.65, 1.15, 8.7, 0.76, {
    fontSize: 38,
    bold: true,
    color: C.white,
  });
  text(slide, 'Quem tem maior chance\nde responder à campanha?', 0.65, 2.0, 8.4, 0.9, {
    fontSize: 25,
    bold: true,
    color: C.pink,
    valign: 'top',
  });
  text(slide, 'Estruturamos a base no Oracle e aprimoramos a Decision Tree para orientar um teste de público.', 0.65, 3.03, 8.5, 0.45, {
    fontSize: 15,
    color: C.body,
  });
  const names = [
    'Giovanni Henrique Pereira Hessel  |  RM 570574',
    'Suellen Pereira da Silva  |  RM 573862',
    'Arthur Zeferino  |  RM 570858',
    'Israel Carneiro de Toledo  |  RM 573854',
  ];
  names.forEach((name, i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    rect(slide, 0.65 + col * 4.45, 3.9 + row * 0.43, 0.05, 0.24, C.pink);
    text(slide, name, 0.82 + col * 4.45, 3.87 + row * 0.43, 4.08, 0.27, {
      fontSize: 11,
      color: C.secondary,
    });
  });
  text(slide, 'SALA 1TIAPZ-2026', 0.65, 5.1, 4.2, 0.2, {
    fontSize: 9,
    color: C.muted,
    charSpacing: 1.2,
  });
  text(slide, '01', 9.12, 5.1, 0.32, 0.2, { fontSize: 10, color: C.secondary, align: 'right' });
}

// 2. A resposta é rara; isso muda a leitura do modelo.
{
  const slide = base('Nem todo cliente responde', 'A pergunta de produto', 2);
  text(slide, 'Queremos priorizar contatos, não\nprever compras com certeza.', 0.65, 1.72, 3.6, 0.8, {
    fontSize: 21,
    bold: true,
    color: C.white,
    valign: 'top',
  });
  text(slide, 'Na base, 334 de 2.240 clientes aceitaram a campanha observada. É a resposta registrada em RESPONSE: 14,9% dos clientes.', 0.65, 2.75, 3.6, 0.9, {
    fontSize: 14,
    color: C.body,
    valign: 'top',
  });
  text(slide, '14,9%', 5.0, 1.74, 3.9, 0.62, { fontSize: 40, bold: true, color: C.pink });
  text(slide, 'responderam', 5.02, 2.34, 2.4, 0.3, { fontSize: 14, color: C.secondary });
  const barX = 5.0;
  const barY = 2.95;
  const barW = 4.25;
  rect(slide, barX, barY, barW, 0.38, C.grey);
  rect(slide, barX, barY, barW * 0.1491, 0.38, C.pink);
  text(slide, '334 responderam', barX, 3.52, 2.0, 0.26, { fontSize: 12, bold: true, color: C.white });
  text(slide, '1.906 não responderam', barX + 2.1, 3.52, 2.15, 0.26, { fontSize: 12, color: C.secondary, align: 'right' });
  rect(slide, 0.65, 4.0, 3.6, 0.7, C.card);
  text(slide, '193 perfis se repetem, somando 201 linhas além da primeira ocorrência.', 0.85, 4.13, 3.2, 0.42, {
    fontSize: 11,
    color: C.body,
  });
  rect(slide, 5.0, 4.16, 4.25, 0.6, C.card);
  text(slide, 'Uma lista curta precisa encontrar respostas sem ignorar quem pode responder.', 5.22, 4.29, 3.8, 0.33, {
    fontSize: 12,
    color: C.body,
  });
}

// 3. Dados estruturados e conferidos tornam a análise reproduzível.
{
  const slide = base('Primeiro, deixamos os dados confiáveis', 'Cognitive Data Science', 3);
  card(slide, 0.65, 1.78, 2.75, 1.38, '2.240 clientes', 'Carga Oracle verificada em 18/09.\n2.240 IDs distintos.', C.pink);
  card(slide, 3.62, 1.78, 2.75, 1.38, '29 campos', 'DataFrame Oracle (2240, 29) verificado em 18/09. Modelo agrupado: validação local com CSV.', C.secondary);
  card(slide, 6.59, 1.78, 2.75, 1.38, '24 rendas ausentes', 'INCOME aceita nulos e a imputação acontece dentro do treino.', C.amber);
  const steps = [
    ['CREATE + ALTER', 'Tabela e constraints'],
    ['INSERT + UPDATE + DELETE', 'Demonstração em tabela separada'],
    ['SELECT', 'DataFrame para o modelo'],
  ];
  steps.forEach((s, i) => {
    const x = 0.65 + i * 3.0;
    rect(slide, x, 3.68, 2.72, 0.88, C.card);
    text(slide, s[0], x + 0.16, 3.85, 2.4, 0.24, { fontSize: 12, bold: true, color: C.pink });
    text(slide, s[1], x + 0.16, 4.18, 2.4, 0.25, { fontSize: 11, color: C.body });
    if (i < 2) {
      text(slide, '→', x + 2.77, 3.96, 0.22, 0.22, { fontSize: 16, bold: true, color: C.secondary, align: 'center' });
    }
  });
  text(slide, 'Mantivemos a tabela principal intacta durante a demonstração das operações DML.', 0.65, 4.75, 8.7, 0.26, {
    fontSize: 11,
    color: C.secondary,
  });
}

// 4. Features com leitura de negócio, sem mistério.
{
  const slide = base('Criamos sinais que fazem sentido para o negócio', 'Feature Engineering', 4);
  card(slide, 0.65, 1.8, 2.75, 2.3, 'Quem é o cliente', 'AGE_AT_2014 = 2014 - YEAR_BIRTH\nTOTAL_CHILDREN = KIDHOME + TEENHOME\n\nIdade e contexto familiar.', C.pink);
  card(slide, 3.62, 1.8, 2.75, 2.3, 'Como compra', 'TOTAL_SPEND = soma por categoria\nWEB_PURCHASE_SHARE = compras web ÷ total\n\nValor e preferência de canal.', C.amber);
  card(slide, 6.59, 1.8, 2.75, 2.3, 'Histórico e vínculo', 'CAMPAIGNS_ACCEPTED: aceites anteriores\nCUSTOMER_TENURE_DAYS: dias desde o cadastro\n\nRespostas passadas e tempo de relação.', C.secondary);
  rect(slide, 0.65, 4.42, 8.69, 0.48, C.card);
  text(slide, 'Não usamos RESPONSE para criar os sinais. O alvo fica reservado para avaliar a árvore.', 0.88, 4.53, 8.2, 0.25, {
    fontSize: 12,
    bold: true,
    color: C.white,
  });
}

// 5. O holdout permanece fora da escolha dos parâmetros.
{
  const slide = base('O teste ficou fora do ajuste', 'Comparação justa', 5);
  text(slide, 'Holdout estratificado 80/20; perfis com preditores iguais ficam no mesmo conjunto.', 0.65, 1.62, 8.6, 0.42, {
    fontSize: 16,
    bold: true,
    color: C.white,
  });
  rect(slide, 0.65, 2.25, 8.69, 0.12, C.grey);
  rect(slide, 0.65, 2.25, 6.95, 0.12, C.pink);
  text(slide, '80%  TREINO', 0.65, 2.52, 3.2, 0.34, { fontSize: 21, bold: true, color: C.pink });
  text(slide, '20%  TESTE', 7.05, 2.52, 2.2, 0.34, { fontSize: 19, bold: true, color: C.white, align: 'right' });
  card(slide, 0.65, 3.08, 4.15, 1.34, 'Só no treino', 'Cinco dobras mantêm a proporção de respostas e perfis iguais juntos. A ROC AUC escolhe a configuração.', C.pink);
  card(slide, 5.12, 3.08, 4.22, 1.34, 'Só no final', 'O teste fica reservado. Comparamos a Decision Tree da aula e a ajustada no mesmo conjunto.', C.secondary);
  text(slide, 'Ajustamos critério, profundidade, mínimo de clientes por folha e peso de classe. Imputação e categorias ficam no pipeline.', 0.65, 4.64, 8.7, 0.28, {
    fontSize: 10,
    color: C.secondary,
  });
}

// 6. Resultados em linguagem de decisão.
{
  const slide = base('Melhor ranking, com uma troca nos contatos', 'Árvore da aula versus árvore ajustada', 6);
  text(slide, 'ROC AUC mede se quem respondeu fica acima de quem não respondeu no ranking.', 0.68, 1.48, 4.45, 0.18, { fontSize: 10, color: C.secondary });
  text(slide, 'Métrica', 0.68, 1.72, 1.25, 0.24, { fontSize: 12, bold: true, color: C.secondary });
  text(slide, 'Referência', 2.2, 1.72, 1.05, 0.24, { fontSize: 11, color: C.secondary, align: 'right' });
  text(slide, 'Ajustada', 3.45, 1.72, 1.05, 0.24, { fontSize: 11, color: C.pink, align: 'right' });
  const metrics = [
    ['Precision', 0.3651, 0.5000],
    ['Recall', 0.3433, 0.3134],
    ['F1', 0.3538, 0.3853],
    ['ROC AUC', 0.6357, 0.7973],
  ];
  metrics.forEach((m, i) => {
    const y = 2.12 + i * 0.58;
    text(slide, m[0], 0.68, y, 1.28, 0.22, { fontSize: 13, color: C.body });
    const bx = 2.2;
    const maxW = 2.0;
    rect(slide, bx, y + 0.01, maxW * m[1], 0.13, C.grey);
    rect(slide, bx, y + 0.2, maxW * m[2], 0.13, C.pink);
    text(slide, m[1].toFixed(4), 4.2, y - 0.02, 0.8, 0.18, { fontSize: 11, color: C.secondary, align: 'right' });
    text(slide, m[2].toFixed(4), 4.2, y + 0.17, 0.8, 0.18, { fontSize: 11, color: C.pink, align: 'right' });
  });
  text(slide, 'Precisão: quantos contatos indicados responderam. Recall: quantos dos que responderam encontramos.', 0.68, 4.46, 4.55, 0.32, { fontSize: 10, color: C.secondary });
  rect(slide, 5.35, 1.78, 3.99, 2.85, C.card);
  rect(slide, 5.35, 1.78, 0.06, 2.85, C.pink);
  text(slide, '+0,1616', 5.67, 2.08, 3.3, 0.64, { fontSize: 34, bold: true, color: C.pink });
  text(slide, 'de ROC AUC', 5.68, 2.72, 2.9, 0.3, { fontSize: 15, color: C.white });
  text(slide, 'Ajustada: 0,7973\nPrecisão subiu. Recall caiu.', 5.68, 3.32, 3.15, 0.65, { fontSize: 14, color: C.body, valign: 'top' });
  text(slide, 'O score ajuda a escolher quem entra no teste. Um grupo de controle mede se a campanha realmente mudou o resultado.', 5.68, 4.05, 3.15, 0.48, { fontSize: 12, color: C.secondary, valign: 'top' });
  text(slide, 'Validação local no CSV. Salvar a execução Oracle agrupada antes da entrega.', 0.65, 4.83, 8.7, 0.22, {
    fontSize: 11,
    color: C.muted,
  });
}

await pptx.writeFile({ fileName: out });
console.log(out);
