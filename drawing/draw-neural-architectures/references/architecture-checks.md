# Architecture checks

Review actual structure before and after drawing; this is not automatic model verification.

## Evidence and abstraction

Record source file/forward method or paper section/revision. Inspect dynamic branching and functional operations, not just registered layers. Separate tensor paths, conditioning, losses and annotations. Choose an abstraction level and label omitted repeated blocks. Never invent parameter counts, widths, weights or results.

For missing facts use C, H, W, N or a named abstract block. Ask only if the choice changes the method. Generic illustrations may use explicitly stated example shapes; the user's model must use verified values.

## CNN and U-Net

- Fix tensor order, normally C × H × W or B × C × H × W.
- For convolution check stride, dilation, padding: output = floor((input + 2p - d(k-1) - 1)/s + 1).
- Addition requires compatible shapes or explicit projection/broadcast. Concat sums the named axis; other axes must agree. Do not replace U-Net concatenation with addition.
- Follow cropping/alignment; valid convolutions or odd inputs may produce mismatched skip sizes.
- Distinguish interpolation + convolution, transposed convolution and pixel shuffle; use generic Upsample only at an abstract level.
- Label numeric shapes when 3D block scale is schematic/logarithmic.

## Transformer and DiT

- Distinguish encoder-only, causal decoder-only and encoder-decoder; identify causal masks.
- Self-attention Q/K/V share a sequence. Cross-attention queries come from the receiving branch; keys/values from context. Label Q and K,V when ambiguous.
- Follow pre-norm versus post-norm. Trace each residual around its intended sublayer. Distinguish embeddings, positions, projections and heads.
- For DiT identify patchification, conditioning, modulation, gates, unpatchification and output parameterization from sources. Generic conditioning is not an implementation of adaLN-Zero, FLUX or SD3.
- Do not infer heads, tokens, sharing or causality from a template.

## Diffusion and flow

- State endpoint/time convention. The bundled generic RF example uses x_t=(1-t)z+t x_HQ, t in [0,1], z~N(0,I), target u=x_HQ-z and inference 0→1. Other methods may reverse time or predict noise, clean image, score, residual, displacement or mean velocity.
- Conditioning image is not automatically the initial state. LQ-as-condition, LQ-initialized paths and residual fields require different diagrams/equations.
- Distinguish training interpolation from inference solver. Mark sampled noise/time and ground truth as training-only where appropriate.
- Show frozen teachers/backbones, detach and trainable adapters only from evidence. Trace gradients when scientifically useful or requested.
- Verify teacher/student paths, stochastic updates, function evaluations and one-step semantics independently for distillation.

## Final reconciliation

Every meaningful arrow needs correct endpoints; losses need predictions/targets; condition routes must terminate at correct modules; annotations must match the method. Visual inspection does not certify a research claim.
